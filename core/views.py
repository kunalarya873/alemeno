from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customer
from django.db.utils import IntegrityError
from .models import Loan
from .utils import calculate_credit_score
from .serializers import RegisterCustomerSerializer
from decimal import Decimal
from datetime import datetime, timedelta


class RegisterCustomerView(APIView):
    def post(self, request):
        serializer = RegisterCustomerSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        monthly_income = data['monthly_income']
        approved_limit = round(monthly_income * 36 / 1_00_000) * 1_00_000

        customer = Customer.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone_number=data['phone_number'],
            monthly_salary=monthly_income,
            approved_limit=approved_limit,
            current_debt=0
        )

        return Response({
            'customer_id': customer.customer_id,
            'name': f"{customer.first_name} {customer.last_name}",
            'age': data['age'],
            'monthly_income': customer.monthly_salary,
            'approved_limit': customer.approved_limit,
            'phone_number': customer.phone_number
        }, status=status.HTTP_201_CREATED)
    
class CheckEligibilityView(APIView):
    def post(self, request):
        try:
            data = request.data
            customer_id = data.get('customer_id')
            loan_amount = data.get('loan_amount')
            interest_rate = data.get('interest_rate')
            tenure = data.get('tenure')

            customer = Customer.objects.get(customer_id=customer_id)
            loan_data = Loan.objects.filter(customer=customer)

            credit_score = calculate_credit_score(customer, loan_data)

            # Determine interest rate slab
            corrected_interest_rate = interest_rate
            if credit_score > 50:
                pass  # Interest rate remains the same
            elif 30 < credit_score <= 50:
                corrected_interest_rate = max(12, interest_rate)
            elif 10 < credit_score <= 30:
                corrected_interest_rate = max(16, interest_rate)
            else:
                return Response({'approval': False, 'message': 'Loan not approved due to low credit score'}, status=status.HTTP_200_OK)

            return Response({
                'customer_id': customer_id,
                'approval': True,
                'interest_rate': interest_rate,
                'corrected_interest_rate': corrected_interest_rate,
                'tenure': tenure,
                'monthly_installment': (loan_amount * corrected_interest_rate / 100) / 12
            }, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateLoanView(APIView):
    def post(self, request):
        try:
            data = request.data
            loan_amount = Decimal(str(data.get('loan_amount')))
            interest_rate = Decimal(str(data.get('interest_rate')))
            tenure = data.get('tenure')
            customer_id = data.get('customer_id')

            # Fetch customer
            customer = Customer.objects.get(customer_id=customer_id)

            # Calculate monthly installment
            monthly_installment = loan_amount * (interest_rate / Decimal(100)) / Decimal(12)

            # Validate debt-to-income ratio
            if monthly_installment > (Decimal(0.5) * customer.monthly_salary):
                return Response({
                    'loan_id': None,
                    'customer_id': customer_id,
                    'loan_approved': False,
                    'message': 'Monthly installment exceeds 50% of salary'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Calculate start_date (current date) and end_date (tenure in months from now)
            start_date = datetime.now()  # Current date
            end_date = start_date + timedelta(days=tenure * 30)  # Approximate end date based on tenure in months

            # Create loan
            loan = Loan.objects.create(
                customer=customer,
                loan_amount=loan_amount,
                interest_rate=interest_rate,
                tenure=tenure,
                monthly_repayment=monthly_installment,
                emis_paid_on_time=0,
                start_date=start_date,
                end_date=end_date
            )

            return Response({
                'loan_id': loan.loan_id,
                'customer_id': customer_id,
                'loan_approved': True,
                'message': 'Loan approved successfully',
                'monthly_installment': monthly_installment
            }, status=status.HTTP_201_CREATED)

        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ViewLoanDetails(APIView):
    def get(self, request, loan_id):
        try:
            loan = Loan.objects.get(loan_id=loan_id)
            customer = loan.customer

            return Response({
                'loan_id': loan.loan_id,
                'customer': {
                    'id': customer.customer_id,
                    'first_name': customer.first_name,
                    'last_name': customer.last_name,
                    'phone_number': customer.phone_number,
                    'age': customer.age
                },
                'loan_amount': loan.loan_amount,
                'interest_rate': loan.interest_rate,
                'monthly_installment': loan.monthly_repayment,
                'tenure': loan.tenure
            }, status=status.HTTP_200_OK)
        except Loan.DoesNotExist:
            return Response({'error': 'Loan not found'}, status=status.HTTP_404_NOT_FOUND)

class ViewLoansByCustomer(APIView):
    def get(self, request, customer_id):
        try:
            customer = Customer.objects.get(customer_id=customer_id)
            loans = Loan.objects.filter(customer=customer)

            loan_data = []
            for loan in loans:
                loan_data.append({
                    'loan_id': loan.loan_id,
                    'loan_amount': loan.loan_amount,
                    'interest_rate': loan.interest_rate,
                    'monthly_installment': loan.monthly_repayment,
                    'repayments_left': loan.tenure - loan.emis_paid_on_time
                })

            return Response(loan_data, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
