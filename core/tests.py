from rest_framework.test import APITestCase
from .models import Customer

class RegisterCustomerTestCase(APITestCase):
    def test_register_customer(self):
        response = self.client.post('/register', {
            'first_name': 'John',
            'last_name': 'Doe',
            'age': 30,
            'monthly_income': 50000,
            'phone_number': '1234567890'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Customer.objects.count(), 1)
