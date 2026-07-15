import math
''' 
make a finance calculator for investments and bonds
for the investments make one for compound and for simple interest
for the bond it is for findingout total monthly payment for a mortgage.
keep it simple and remeber the lessons and training. 
'''
# adding .lower() will make it so no matter how they type investment or bond it will move them to the next step.
define_finance_calculator = input("Investment - to Calculate the amount of interest you'll earn on your investment. "
                           " "
                           "Bond - to calculate the amount you'll pay on a home loan." 
                           " "
                           "Enter either 'investment' or 'bond' from the menu above to proceed: ").lower()

if define_finance_calculator == 'investment':
    P = float(input("The amount of money being deposited: "))
    # Dividing the interest rate by 100 to handle percentage input correctly
    r = float(input("The interest rate: ")) / 100
    t = int(input("The number of years you plan to invest: "))

    interest_type = input("Please enter if you want 'simple' or 'compound' interest: ").lower()

    if interest_type == 'simple':
        A = P * (1 + r * t)
        #adding in the :.2f makes it so that the value is rounded to two decimal places.
        print(f"The total amount of your investment will be: {A:.2f}")
    elif interest_type == 'compound':
        # Compound interest calculation goes here
        A = P * math.pow((1 + r), t)
        print(f"The total amount of your investment will be: {A:.2f}")
    else:
        print("Invalid interest type entered. Please choose 'simple' or 'compound'.")
elif define_finance_calculator == 'bond':
    # Bond calculation goes here
    P = float(input("The current value of the house: "))
    # divide by 100 to get the rate and then by 12 again to split it up for the months
    i = float(input("The interest rate: ")) / 100 / 12
    n = int(input("The number of months you plan to take to repay the bond: "))
    repayment = (i * P) / (1 - (1 + i) ** (-n))
    print(f"The monthly repayment amount will be: {repayment:.2f}")
else:
    print("Invalid option selected. Please choose 'investment' or 'bond'.")
