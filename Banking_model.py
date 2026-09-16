from abc import ABC, abstractmethod


class Account(ABC):

    def __init__(self, account_number, balance):
        self.account_number = account_number
        self._balance = balance

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount

    def withdraw(self, amount):
        if 0 < amount <= self._balance:
            self._balance -= amount
            return True
        return False

    def get_balance(self):
        return self._balance

    @abstractmethod
    def process_monthly(self):
        pass


class SavingsAccount(Account):

    def __init__(self, account_number, balance, interest_rate=0.02):
        super().__init__(account_number, balance)
        self.interest_rate = interest_rate

    def process_monthly(self):
        benefit = self._balance * self.interest_rate
        self.deposit(benefit)


class CurrentAccount(Account):

    def __init__(self, account_number, balance, fee=5.0):
        super().__init__(account_number, balance)
        self.fee = fee

    def process_monthly(self):
        self._balance -= self.fee


accounts = [
    SavingsAccount("SAV101", 1000.0),
    CurrentAccount("CUR102", 500.0),
]

for acc in accounts:
    acc.deposit(200)
    acc.withdraw(50)
    acc.process_monthly()
    print(f"Account {acc.account_number} balance: {acc.get_balance()}")