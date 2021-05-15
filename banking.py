# Write your code here
from random import randint
from sqlite3 import *

# I should have used **{conn = sqlite3.connect('card.s3db')}** but we have imported * from sqlite3
conn = connect('card.s3db')  # sqlite3.connect(':memory:') refreshed in-memory db
c = conn.cursor()


def create_table():
    c.execute("""CREATE TABLE card(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number TEXT,
            pin TEXT,
            balance INTEGER DEFAULT 0
            )""")


def luhn_valid(acct):
    g = int(acct[-1])
    v1 = list(map(int, list(acct[:15])))
    v2, count = [], 1
    for i in v1:
        if count % 2 == 0:
            v2.append(i)
        else:
            v2.append(2 * i)
        count += 1
    v3 = [j - 9 if j > 9 else j for j in v2]
    d = sum(v3) + g
    return True if d % 10 == 0 else False


class Bank:
    def __init__(self):
        self.acct_num, self.pin = None, None    # to be used for login confirmation
        self.m, self.n = None, None             # to be used when creating account details
        self.balance = 0                        # to keep account of account balance
        self.acc_num, self.bal = None, 0     # to keep track of balance change during transfer

    def gen_num0(self):
        self.m = '400000' + '%0.10d' % (randint(0000000000, 9999999999))
        return self.m if luhn_valid(self.m) else self.gen_num0()
    # account number generated i.e. self.m

    def gen_num1(self):
        self.n = '%0.4d' % (randint(0, 9999))
        return self.n
    # account pin generated i.e. self.n

    def create_acct(self):
        print('Your card has been created')
        print(f'Your card number:\n{self.gen_num0()}')
        print(f'Your card PIN:\n{self.gen_num1()}')
        self.insert_acct()
        self.task1()

    def insert_acct(self):
        with conn:
            c.execute(f"INSERT INTO card ('number', 'pin', 'balance') "
                      f"VALUES ({self.m}, {self.n}, 0)")
            # self.m, self.n and default balance uploaded to the database
            conn.commit()

    def update_acct(self, y, z):
        with conn:
            # y = new balance, z = account number to be updated
            c.execute(f'UPDATE card SET balance = {y} where number = {z}')
            conn.commit()

    def delete_acct(self, a_n, p_n):
        with conn:
            c.execute(f'DELETE FROM card WHERE number = {a_n} and pin = {p_n}')
            conn.commit()

    def money_in_out(self, inc):
        if self.balance + inc >= 0:
            self.balance += inc
            if inc < 0:
                self.bal -= inc
        else:
            print('Not enough money!')
            self.task2()

    def get_acct1(self, ac_num, p_num):
        c.execute(f'SELECT * from card WHERE number = {ac_num} and pin ={p_num}')
        lst = c.fetchall()
        return True if len(lst) > 0 else False

    def get_acct2(self, ac_num):
        c.execute(f'SELECT * from card WHERE number = {ac_num}')
        lst = c.fetchall()
        return True if len(lst) > 0 else False

    def log_in(self):
        # print(acct_num, pin)
        print('Enter your card number:')
        self.acct_num = input()
        print('Enter your PIN:')
        self.pin = input()
        if self.get_acct1(self.acct_num, self.pin):
            print('You have successfully logged in!')
            # logged in with available acct number and pin and saved
            self.task2()
        else:
            print('Wrong card number or PIN!')
            self.task1()

    def task1(self):
        print("1. Create an account\n"
              "2. Log into account\n"
              "0. Exit")
        t1 = int(input())
        if t1 == 1:
            self.create_acct()
        elif t1 == 2:
            self.log_in()
        else:
            print('Bye!')
            exit()

    def task2(self):
        print("1. Balance\n"
              "2. Add income\n"
              "3. Do transfer\n"
              "4. Close account\n"
              "5. Log out\n"
              "0. Exit")
        t2 = int(input())
        if t2 == 1:
            print('Balance:', self.balance)
            self.task2()
        elif t2 == 2:
            print('Enter income:')
            mon = int(input())
            self.money_in_out(mon)
            print('Income was added')
            self.update_acct(self.balance, self.acct_num)
            self.task2()
        elif t2 == 3:
            print('Transfer\n'
                  'Enter card number:')
            self.acc_num = input()
            if luhn_valid(self.acc_num):
                if self.get_acct2(self.acc_num):
                    print('Enter how much money you want to transfer:')
                    tue = -1 * int(input())
                    self.money_in_out(tue)
                    print('Success!')
                    self.update_acct(self.balance, self.acct_num)
                    self.update_acct(self.bal, self.acc_num)
                    self.task2()
                else:
                    print('Such a card does not exist.')
                    self.task2()
            else:
                print('Probably you made a mistake in the card number.\n'
                      'Please try again!')
                self.task2()
        elif t2 == 4:
            self.delete_acct(self.acct_num, self.pin)
            print('The account has been closed!')
            self.task1()
        elif t2 == 5:
            print('You have successfully logged out!')
            self.task1()
        else:
            print('Bye!')
            exit()


if __name__ == '__main__':
    ali = Bank()
    # c.execute('DROP TABLE card')
    try:
        create_table()
    except OperationalError:
        # pass
        ali.task1()
    finally:
        conn.commit()
        conn.close()
