
def calculate_credit_score(customer, loan_data):
    if customer.current_debt > customer.approved_limit:
        return 0  # Credit score is 0 if current debt exceeds approved limit.

    score = 50  # Base score
    past_loans = loan_data.filter(customer=customer)

    score += len(past_loans) * 5
    score += sum(loan.emis_paid_on_time for loan in past_loans)

    return min(score, 100)  # Max credit score is 100.
