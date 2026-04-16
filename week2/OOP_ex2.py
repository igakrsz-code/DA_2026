# 1
class Currency:
    def __init__(self, currency, amount):
        self.currency = currency
        self.amount = amount

    def __str__(self):
        return f"{self.amount} {self.currency}s"

    def __repr__(self):
        return f"{self.amount} {self.currency}s"

    def __int__(self):
        return self.amount

    def __add__(self, other):
        if isinstance(other, int):
            return self.amount + other

        if isinstance(other, Currency):
            if self.currency != other.currency:
                raise TypeError(
                    f"Cannot add between Currency type <{self.currency}> and <{other.currency}>"
                )
            return self.amount + other.amount

        raise TypeError("Unsupported type")

    def __iadd__(self, other):
        if isinstance(other, int):
            self.amount += other

        elif isinstance(other, Currency):
            if self.currency != other.currency:
                raise TypeError(
                    f"Cannot add between Currency type <{self.currency}> and <{other.currency}>"
                )
            self.amount += other.amount
        else:
            raise TypeError("Unsupported type")

        return self



#2

def sum_numbers(a, b):
    print(a + b)
from func import sum_numbers

sum_numbers(5, 7)

# 3
import random
import string

letters = string.ascii_letters

result = ""
for _ in range(5):
    result += random.choice(letters)

print(result)

#4
from datetime import datetime

def show_date():
    today = datetime.today()
    print(today.date())

show_date()


# 5
from datetime import datetime

def time_until_new_year():
    now = datetime.now()
    next_year = datetime(now.year + 1, 1, 1)

    diff = next_year - now
    print(diff)

time_until_new_year()


# 6
from datetime import datetime

def minutes_lived(birthdate_str):
    birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d")
    now = datetime.now()

    diff = now - birthdate
    minutes = int(diff.total_seconds() / 60)

    print(f"You lived {minutes} minutes")

minutes_lived("2000-01-01")


# 7
from faker import Faker

fake = Faker()
users = []

def add_users(n):
    for _ in range(n):
        user = {
            "name": fake.name(),
            "address": fake.address(),
            "language_code": fake.language_code()
        }
        users.append(user)

add_users(3)

for user in users:
    print(user)



