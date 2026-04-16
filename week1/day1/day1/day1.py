greetings = "Hello, World!"
print(type(greetings))
print(type('hi'))
print(type(123))
print(type("123"))

#string method
print(greetings.upper())
print(greetings.lower())
print(len(greetings))

# string concatentation - joining two strings together
first_name = "John"
last_name = "Doe"
full_name = first_name + " " + last_name
print(full_name)

print(' Ha ' * 3) # string repetition - hahaha

test = "   Hello, World!   "
print(test.replace("world", "Python")) # string replacement
print(test)
print(test.count("l")) # for the original one

multiline = """"
line 1
line 2
"""
print(multiline)

print(test[0]) # indexing - H
print(test[-1])

# numbers
# ingers - numbers without decimal points
age = 25
temp = 25
year = 2026
print(type(year))

# float - numbers with decimal points
price = 19.99
pi = 3.14
print(type(price))

# boolean - True or False
is_sunny = True
is_raining = False 
print(type(is_sunny))
print(type(is_raining))
print ( 5 > 3) # comparison operator - True
print ( 5 < 3) # False
print( 7 == 7) # True
print( 7 != 7) # False - not equal to

# Comparison operators:
# == is used for comparison, while = is used for assignment.
# !# is not equal to operator, used for comparison. It checks if two values are not equal and returns True if they are not equal, and False if they are equal.
# >= is greater than or equal to operator, used for comparison. It checks if the value on the left is greater than or equal to the value on the right and returns True if it is, and False if it is not.

# logical operators:
# and - returns True if both conditions are true
# or - returns True if at least one condition is true
# not - returns the opposite of the condition
print( True and True) # True
print( True or False) # True
print (False or True) # True
print (not True) # False
print (not False) # True

x = 42
y = "42"
print(x + 1) # 43
print(y + "1") # 421 - string concatenation
print (y + 1) # TypeError - cannot concatenate str and int

# type casting - converting one data type to another
str_num = "100" # it's a string
print(str_num + 1) # TypeError - cannot concatenate str and int
print(int(str_num) + 1) # 101 - string to integer
# u can do it only if you have numbers in the string, otherwise it will raise an error

num = 42
print(num + ' is the answer ') # TypeError - cannot concatenate int and str
print(str(num) + ' is the answer ') # 42 is the answer - integer to string

print(bool(1)) # True - non-zero numbers are considered True
print(bool(0)) # False - zero is considered False
print(bool(-1)) # True - non-zero numbers are considered True
print(bool("")) # False - empty string is considered False
print(bool(" ")) # True - non-empty string is considered True

# variables - used to store data
name = "Alice"
age = 25
height = 186.3
is_student = True
max_attempts = 5
# you cannot start a variable name with a number, but you can use underscores
# but something like n2me is ok, but 2name is not
# also no - in variable names, but you can use underscores like max_attempts
# dont call it reserved keywords like print, str, int, etc.

a = 1
b = 2
c = 3
a,b,c = 1,2,3 # multiple assignment

a,b = b,a # swapping values
print(a) # 2
print(b) # 1

# incrementing
counter = 0
counter = counter + 1 # 1
counter +=1 # 2 - shorthand for incrementing
print(counter) # 2

# string formatting - inserting variables into strings
first = "John"
last = "Doe"
text1 = "Hello," + " " + first + " " + last
print(text1) # Hello, John Doe

text3 = "Hello, {} {}".format(first, last)
print(text3) # Hello, John Doe 
# this is the older way of string formatting

text4 = f"Hello, {first} {last}"
print(text4) # Hello, John Doe
# this is the newer way of string formatting, using f-strings
# f-strings are more readable and easier to use than the older format method, and they also allow for inline expressions, making them more powerful and flexible for string formatting tasks.

price = 19.99
quantity = 3
total = f"Total price: ${price * quantity}"
print(total) # Total price: $59.97

pi = 3.14159
print(f"{pi:.2f}") # 3.14 - formatting pi to 2 decimal places
# 2f means 2 decimal places (2 numbers after the dot), and f means float.
# 3 You can also use d for integers, s for strings, etc.

name = input("Enter your name: ")
print(f"Hello, {name}!")
# The input function is used to get user input from the console. 
# It takes a string as an argument, which is displayed as a prompt to the user. 
# The function returns the user's input as a string. 
# In this example, we ask the user to enter their name and then greet them using an f-string to format the output.
age= input("Enter your age: ")
print(f"You are {age} years old.")

age = int(input("Enter your age: "))
print(f"You are {age} years old.")
# In this example, we use the int() function to convert the user's input from a string to an integer.

# if statements - used for conditional execution of code
age = 18
if age >= 18:
    print("You are an adult.") 
    print("Finish") # this will be executed if the condition is true

score = 85
if score >= 90 or score == 100:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
# In this example, we use if, elif, and else statements to determine the grade based on the score.
else:
    grade = "F"
    
#print(grade)
has_license = True
if not has_license:
    print("No")
else:    print("Yes")

hobbies = " coding, reading, hiking "
if "coding" in hobbies:
    print("You like coding!")  
    # The in operator is used to check if a substring is present in a string.
    #if "a" in apple:
      #  print("Yes")
        

# nested conditions
my_age = 18
has_license = True
if my_age >= 18:
    if has_license:
        print("You can drive!")
    else:
        print("You need a license to drive.")
else:
    print("You are too young to drive.")

# Ternary operator - a shorthand for if-else statements
status = "adult" if age >= 18 else "minor"
print(status) # adult










 






