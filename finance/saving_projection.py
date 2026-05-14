from datetime import date, datetime, timedelta


# Current date and time
now = datetime.now()
today = now.date()
weekday_name = now.strftime("%A")

# Calculate the next Monday
days_ahead = (0 - today.weekday() + 7) % 7
next_monday = today + timedelta(days=days_ahead)

#--------------- Constants ------------------
index_avg_return = 0.065
savings_avg_return = 0.026
today = date.today()
one_year = today + timedelta(days=365)

def ask_future_date(prompt="Enter next paycheck date (MM-DD-YYYY): "):
    while True:
        s = input(prompt).strip()
        try:
            d = datetime.strptime(s, "%m-%d-%Y").date()
        except ValueError:
            print("Invalid format. Use MM-DD-YYYY.")
            continue

        if d <= today:
            print("Please pick a date after today.")
        elif d > one_year:
            print("Please pick a date within the next 12 months.")
        else:
            return d


def calculate_interest_index(total, weeks_between_paychecks):
    # interest for one paycheck period
    period_rate = index_avg_return * (weeks_between_paychecks / 52.0)
    return total * period_rate

def calculate_interest_saving(total, weeks_between_paychecks):
    # interest for one paycheck period
    period_rate = savings_avg_return * (weeks_between_paychecks / 52.0)
    return total * period_rate


def main():
    saving_amounts = []
    print("\n===================================================================================")
    starting_amount = float(input("Starting bank account amount: $"))
    paycheck_count = int(input("How many paychecks a year do you get? "))
    weeks_between_paychecks = 52.0/paycheck_count
    investment_length = int(input("How many years will you invest? "))
    initial_paycheck_date = ask_future_date()
    num_days = round(investment_length * 365.25)
    last_paycheck = initial_paycheck_date + timedelta(days=num_days)
    print("Input amount you want to save per paycheck. type 'done' when you are done adding values to test.\n")
    while True:
        saving_amount = input("Dollar amount to contribute: $").strip().lower()
        if saving_amount == "done":
            break
        if saving_amount =="":
            continue
        
        try:
            amount = int(saving_amount)
        except ValueError:
            print("enter a whole number. ie. 100")
            continue
        
        saving_amounts.append(amount)
    
    for contribution in saving_amounts:
        incremental_date = initial_paycheck_date
        index_total = starting_amount
        sav_total = starting_amount
        while incremental_date < last_paycheck:
            index_total = index_total + contribution + calculate_interest_index(index_total, weeks_between_paychecks)
            sav_total = sav_total + contribution + calculate_interest_saving(sav_total,weeks_between_paychecks)
            incremental_date = incremental_date + timedelta(weeks=weeks_between_paychecks)
        print("\n==========================================================================================================")
        print(f"Contributing ${contribution} every paycheck which is recieved approximately every {round(weeks_between_paychecks,2)} weeks for {investment_length} years will result in...")
        print(f"---> if contributed to a 'low risk' index fund would result in ${round(index_total,2)} by {last_paycheck} if it stays at an average {index_avg_return*100}% return")
        print(f"---> if contributed to high yield savings account would result in ${round(sav_total,2)} by {last_paycheck} if it stays at an average {savings_avg_return*100}% return")
        print("==========================================================================================================\n")

    
if __name__ == "__main__":
    main()