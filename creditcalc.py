from math import ceil, floor, log
import argparse
import sys


def annuity_pmt(P, n, i):
    ans1 = P * (i * pow(1 + i, n)) / (pow(1 + i, n) - 1)
    return [ans1, f'Your monthly payment = {ceil(ans1)}!']


def loan_principal(A, n, i):
    ans2 = A * (pow(1 + i, n) - 1) / (i * pow(1 + i, n))
    return [ans2, (f'Your loan principal = {int(ans2)}!'
                   if int(ans2) == ans2 else f'Your loan principal = {floor(ans2)}!')]


def monthly_num(P, A, i):
    ans3 = ceil(log((A / (A - i * P)), 1 + i))
    ans3b = ''
    yr, mnt = ans3 // 12, ans3 % 12
    if yr > 1:
        if mnt > 1:
            ans3b = f'It will take {yr} years and {mnt} months to repay this loan!'
        elif mnt == 0:
            ans3b = f'It will take {yr} years to repay this loan!'
        elif mnt == 1:
            ans3b = f'It will take {yr} years and 1 month to repay this loan!'
    elif yr == 1:
        if mnt > 1:
            ans3b = f'It will take 1 year and {mnt} months to repay this loan!'
        elif mnt == 0:
            ans3b = f'It will take 1 year to repay this loan!'
        elif mnt == 1:
            ans3b = f'It will take 1 year and 1 month to repay this loan!'
    elif yr == 0:
        if mnt > 1:
            ans3b = f'It will take {mnt} months to repay this loan!'
        elif mnt == 0:
            ans3b = f'It will take to repay this loan!'
        elif mnt == 1:
            ans3b = f'It will take 1 month to repay this loan!'
    return [ans3, ans3b]


def diff_pay(p, n, i):
    payed = 0
    for m in range(n):
        Dm = (p/n) + i * (p-(p*m/n))
        print(f'Month {m+1}: payment is {ceil(Dm)}')
        payed += ceil(Dm)
    print(f'Overpayment = {int(payed-p)}')


parser = argparse.ArgumentParser()
parser.add_argument('--type', type=str, choices=['annuity', 'diff'],
                    help='the type of calculation to be made')
parser.add_argument('--principal', type=float, help='initial amount')
parser.add_argument('--payment', type=float, help='constant payment')
parser.add_argument('--periods', type=int, help='loan duration')
parser.add_argument('--interest', type=float, help='interest rate')

args1 = parser.parse_args()
# print(args1)
args2 = sys.argv
# print(args2)
# print(len(args2))

typ = args1.type                # 'diff', 'annuity',
principal = args1.principal     # 10000000, 500000, 1000000
periods = args1.periods         # 10  # 60, 120
interest = args1.interest
annuity = args1.payment         # 23000
param = [principal, periods, interest, annuity]
par = [i < 0 for i in param if i is not None]

if len(args2) != 5:
    print('Incorrect parameters')
elif typ is None:
    print('Incorrect parameters')
elif interest is None:
    print('Incorrect parameters')
elif any(par):
    print('Incorrect parameters')
elif typ == 'diff':
    if annuity:
        print('Incorrect parameters')
    else:
        interest /= 1200  # converting the annual interest to monthly decimal value
        diff_pay(principal, periods, interest)
elif typ == 'annuity':
    interest /= 1200  # converting the annual interest to monthly decimal value
    if annuity and periods and interest:
        # if all(annuity, periods, interest):
        Pr = loan_principal(annuity, periods, interest)
        print(Pr[1])
        print(f'Overpayment = {int(annuity * periods - floor(Pr[0]))}')
    elif principal and periods and interest:
        # if all(principal, periods, interest):
        ann = annuity_pmt(principal, periods, interest)
        print(ann[1])
        print(f'Overpayment = {int(ceil(ann[0]) * periods - principal)}')
    elif principal and annuity and interest:
        # if all(principal, annuity, interest):
        time = monthly_num(principal, annuity, interest)
        print(time[1])
        print(f'Overpayment = {int(annuity * time[0] - principal)}')
