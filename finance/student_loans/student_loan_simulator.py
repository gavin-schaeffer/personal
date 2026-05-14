#--------------getting time-----------------
from datetime import date, datetime
def add_one_month(d):
    year = d.year + (d.month // 12) 
    month = d.month % 12 + 1
    return date(year, month, d.day)
def minus_one_month(d):
    year = d.year + (d.month // 12) 
    month = d.month % 12 - 1
    return date(year, month, d.day)
#----------------------simulating loan----------------
def simulate_loans(current_loan_balance, total_payment):
    loans = [
    {"name": "1-01 sub","balance": current_loan_balance[0], "rate": 0.0428, "percent total payment": 0.1215},
    {"name": "1-02 unsub","balance": current_loan_balance[1], "rate": 0.0428, "percent total payment":  0.0712},
    {"name": "1-03 sub","balance": current_loan_balance[2], "rate": 0.025, "percent total payment": 0.1434},
    {"name": "1-04 unsub","balance": current_loan_balance[3], "rate": 0.025, "percent total payment": 0.1460},
    {"name": "1-05 sub","balance": current_loan_balance[4], "rate": 0.0348, "percent total payment": 0.1838},
    {"name": "1-06 unsub","balance": current_loan_balance[5], "rate": 0.0348, "percent total payment": 0.0673},
    {"name": "1-07 sub","balance": current_loan_balance[6], "rate": 0.0474, "percent total payment": 0.1951},
    {"name": "1-08 unsub","balance": current_loan_balance[7], "rate": 0.0474, "percent total payment": 0.0716},
]
    today = datetime.now()
    payment_due_date = today.replace(day=5)
    if today > payment_due_date:
        start_date = payment_due_date
    else:
        start_date = minus_one_month(payment_due_date)
    
    #--------------------First lines------------------
    print(f"\n =============================================================")
    print(f"Total Contribution: ${total_payment}/month")

    interest_paid = 0 #initialize Interest paid
    number_of_starting_loans = len(loans)
    difference_list = []

    while any(loan["balance"] > 0 for loan in loans):
        start_date = add_one_month(start_date)
        
        # Only consider active loans
        active_loans = [l for l in loans if l["balance"] > 0]
        number_of_active_loans = len(active_loans)
        difference_list.append(number_of_starting_loans - number_of_active_loans)

        # Normalize weights for remaining loans
        total_weight = sum(l["percent total payment"] for l in active_loans)
        
        #print new loan Values
        if difference_list[-1] == 0 and len(difference_list) == 1:
            print(f"\n Starting payment values as of {start_date}:")
            for loan in active_loans:
                print(f"{loan["name"]} asjusted payment: ${round((loan["percent total payment"]*total_payment),2)} ------> current balance: ${round(loan["balance"],2)}")
        elif difference_list[-1] > 1 and difference_list[-1] != difference_list[-2]:
            print(f"\n new payment values as of {start_date}:")
            for loan in active_loans:
                print(f"{loan["name"]} asjusted payment: ${round((loan["percent total payment"]*total_payment),2)} ------> current balance: ${round(loan["balance"],2)}")

        for loan in active_loans:
            monthly_rate = loan["rate"] / 12

            # Apply interest
            loan["balance"] *= (1 + monthly_rate)
            interest = loan["balance"] * (monthly_rate)
            interest_paid = interest_paid + interest

            # Reallocated payment
            payment = total_payment * (loan["percent total payment"] / total_weight)

            # Cap payment so balance never goes negative
            payment = min(payment, loan["balance"])

            loan["balance"] -= payment
    print(f"-------------------------------------------------------------")
    print(f"\n you will pay ${round(interest_paid,2)} in interest, and pay your last loan on {start_date}")
    print(f"\n =============================================================================================")
    return interest_paid, start_date

def interest_analysis(total_payment,interest_paid, baseline_interest_paid, baseline_start_date, savings_contributions, savings_total_in):
    #gathering dates & timelines
    today = datetime.now()
    def calculate_month_difference(date1, date2):
        # Calculate the differences in years and months
        year_diff =  date1.year - date2.year
        month_diff = date1.month - date2.month

        # Total months
        total_months = year_diff * 12 + month_diff
        return total_months
    baseline_loan_term = calculate_month_difference(baseline_start_date, today)
    proposed_loan_term = calculate_month_difference(start_date, today)
    left_over_time_for_investing = calculate_month_difference(baseline_start_date, start_date)
    #setting variable contants
    proposed_savings_acct_total = savings_total_in
    proposed_total_sav_acct_interest = 0
    baseline_savings_acct_total = savings_total_in
    baseline_total_sav_acct_interest = 0
    savings_acct_interest_rate = 0.033
    extra_money = total_payment[0] -  total_payment[1]
    #calculating interest differences
    loan_interest_saved = baseline_interest_paid - interest_paid
    print(f"\n =============================================================================================")
    print(f"Total Payment is ${total_payment[0]} ---> ${extra_money} over the minimum payment ($300)")
    print(f"making this over-payment each month saves ${round(loan_interest_saved,2)} of interest in total and completes the loan repayment by {start_date}")
    print(f"This leaves {left_over_time_for_investing} months to invest the original minimum of ${total_payment[1]}/month")
    adjustment = 0
    if total_payment[0] >= 10000:
        proposed_savings_acct_total = proposed_savings_acct_total - total_payment[0]
    if 2000> total_payment[0]> 700:
        adjustment = 700 - total_payment[0]
    elif 300>= total_payment[0] >= 700:
        adjustment = 700 - total_payment[0]
    else:
        adjustment = 0

    while proposed_loan_term > 0:
        proposed_loan_term -= 1
        proposed_savings_acct_total = proposed_savings_acct_total + savings_contributions[1] + adjustment
        proposed_interest = proposed_savings_acct_total * (savings_acct_interest_rate/12)
        proposed_total_sav_acct_interest = proposed_total_sav_acct_interest + proposed_interest
        proposed_savings_acct_total = proposed_savings_acct_total + proposed_interest
    while left_over_time_for_investing > 0:
        left_over_time_for_investing -= 1
        proposed_savings_acct_total = proposed_savings_acct_total + savings_contributions[0] + savings_contributions[1] + total_payment[1]
        proposed_interest = proposed_savings_acct_total * (savings_acct_interest_rate/12)
        proposed_total_sav_acct_interest = proposed_total_sav_acct_interest + proposed_interest
        proposed_savings_acct_total = proposed_savings_acct_total + proposed_interest
    
    while baseline_loan_term > 0:
        baseline_loan_term -= 1
        baseline_savings_acct_total = baseline_savings_acct_total + savings_contributions[0] + savings_contributions[1]
        baseline_interest = baseline_savings_acct_total * (savings_acct_interest_rate/12)
        baseline_total_sav_acct_interest = baseline_total_sav_acct_interest +  baseline_interest
        baseline_savings_acct_total = baseline_savings_acct_total + baseline_interest

    print(f"Investing that money over that amount of time into a high yield savings account at {round((savings_acct_interest_rate*100),2)}% would result in ${round(proposed_total_sav_acct_interest,2)} of interest accrued")
    print(f"\n Instead if you only paid the minimum and took the ${extra_money} and... ")
    print(f"Invested that into the same high yield savings account at {round((savings_acct_interest_rate*100),2)}%, you would have made ${round(baseline_total_sav_acct_interest,2)} in interest.") 
    print(f"\nIf we consider the true amount of interest accrued the difference would be...")
    print(f"the interest saved from paying the loan off early would be ${round(loan_interest_saved,2)} plus the interest made after paying off the loans is ${round(proposed_total_sav_acct_interest)} is ${round((loan_interest_saved+proposed_total_sav_acct_interest),2)}")    

    if (loan_interest_saved + proposed_total_sav_acct_interest)  > baseline_total_sav_acct_interest:
        difference = (loan_interest_saved + proposed_total_sav_acct_interest) - baseline_total_sav_acct_interest
        print(f"compared to the ${round(baseline_total_sav_acct_interest)} that could be made by making the minimum shows that we SAVE money with the difference being ${round(difference,2)}")
        print(f"\n =============================================================================================")
    else:
        difference = baseline_total_sav_acct_interest - (loan_interest_saved + proposed_total_sav_acct_interest) 
        print(f"compared to the ${round(baseline_total_sav_acct_interest)} that could be made by making the minimum shows that we LOSE money with the difference being ${round(difference,2)}")
        print(f"\n =============================================================================================")



savings_contributions = [int(input("Gavin Savings Contributions: ")), int(input("Sophia Savings Contributions: "))]
savings_total_in = int(input("How Much is in the savings?: "))
total_payment = [float(input("Planned total amount paid each month: ")), 300]
#current_loan_balance = [
    #float(input("1-01 sub current balance: ")),
    #float(input("1-02 unsub current balance: ")),
    #float(input("1-03 sub current balance: ")),
    #float(input("1-04 unsub current balance: ")),
    #float(input("1-05 sub current balance: ")),
    #float(input("1-06 unsub current balance: ")),
    #float(input("1-07 sub current balance: ")),
    #float(input("1-08 unsub current balance: ")),
#]
current_loan_balance = [
    2857.39,
    1673.45,
    3609.08,
    660.92,
    4408.33,
    1593.11,
    4488.60,
    1613.70,
]
interest_paid , start_date= simulate_loans(current_loan_balance, total_payment[0])
baseline_interest_paid, baseline_start_date = simulate_loans(current_loan_balance, total_payment[1])
interest_analysis(total_payment,interest_paid, baseline_interest_paid, baseline_start_date, savings_contributions, savings_total_in)