# 1
first = "Hello World"

# 2 
# This is a comment

# 3
print("I AM A COMPUTER")

# 4
if 1 < 2 and 4 > 2:
print("Math is fun")

# 5 
x = nope
print(x)

# 6
result = True and False
print(result)

# 7
string = "What's my lenght"
print(len(string))

# 8
string = "I am shouting"
string.upper()
print(string)

# 9
s = "1000"
number = int(s)
print(number)
print(type(number))

# 10
words = ['4', 'real']
sentence = '' .join(words)
print(sentence)

# 11
coolcoolcool

# 12
0

# 13
empty list

# 14
name = input("What is your name? ")
print("Hi," name)

# 15
number = int(input("choose a number"))

if number >= 0:
    print("That number is greater than 0")
else:
    print("You picked 0!")

# 16
fruit = "apple"
index_of_l = fruit.index("l")
print(index_of_l)


# 17
instrument = "xylophone"
instrument.find("y")

# 18
my_string = "Hello"
if my_string.islower() :
    print("Wrong")
else:
    print("False")

# ex 2
def calculate_pet_years(human_years):
    if human_years == 1:
        cat_years = 15
    elif human_years == 2:
        cat_years = 15 + 9
    else:
        cat_years = 15 + 9 + (human_years - 2) * 4

    if human_years == 1:
        dog_years = 15
    elif human_years == 2:
        dog_years = 15 + 9
    else:
        dog_years = 15 + 9 + (human_years - 2) * 5

    return [human_years, cat_years, dog_years]

test_values = [10, 1, 2]

for human_years in test_values:
    print(calculate_pet_years(human_years))

