import math
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--type",
                    choices=["annuity", "diff"],
                    help="You need to choose only one ingredient from the list.")
parser.add_argument("--payment", default=0)
parser.add_argument("--principal", default=0)
parser.add_argument("--periods", default=0)
parser.add_argument("--interest", default=0)

args = parser.parse_args()
if (not args.type) or (args.type not in ["annuity", "diff"]):
    print("Incorrect parameters")
    print("a")
    exit(0)
elif (args.type == "diff") and (args.payment != 0):
    print("Incorrect parameters")
    exit(0)

try:
    type_ = args.type
    principal = float(args.principal)
    payment = float(args.payment)
    periods = int(args.periods)
    interest = float(args.interest)
except (TypeError, NameError):
    print("Incorrect parameters")
    exit(0)

if interest <= 0:
    print("Incorrect parameters")
    exit(0)

# principal
if not (((type_ == "annuity")
        and (((principal == 0) and (periods > 0) and (payment > 0))
             or ((periods == 0) and (principal > 0) and (payment > 0))
             or ((payment == 0) and (principal > 0) and (periods > 0))))
        or ((type_ == "diff") and (principal > 0) and (periods > 0))):
    print("Incorrect parameters")
    exit(0)

interest = interest / 12 / 100
if type_ == "annuity":
    if principal == 0:
        principal = math.ceil(payment / ((interest * (1 + interest) ** periods) / ((1 + interest) ** periods - 1)))
        print("Your loan principal = {}!".format(principal))
    elif payment == 0:
        payment = math.ceil(principal * (interest * (1 + interest) ** periods) / ((1 + interest) ** periods - 1))
        print("Your monthly payment = {}!".format(payment))
    elif periods == 0:
        periods = math.ceil(math.log(payment / (payment - interest * principal), interest + 1))
        string_years = ""
        string_months = ""
        plural_m = ""

        months = periods % 12
        if periods > 11:
            years = periods // 12
            if years == 1:
                plural = ""
            else:
                plural = "s"
            string_years = " {} year{} ".format(years, plural)
        if months > 0:
            and_ = ""
            if months > 1:
                plural_m = "s"
            if years > 0:
                and_ = "and "
            string_months = " {}{}month{}".format(and_, months, plural_m)
        print("It will take{}{}to repay this loan!".format(string_years, string_months))
        overp = int(periods * payment - principal)
        print(f"Overpayment = {overp}")
elif type_ == "diff":
    total = 0
    for m in range(1, periods+1):
        diff_payment_m = math.ceil((principal / periods) + interest * (principal - (principal * (m - 1) / periods)))
        total += diff_payment_m
        print(f"Month {m + 1}: payment is {diff_payment_m}")
    print(f"Overpayment = {int(total - principal)}")
