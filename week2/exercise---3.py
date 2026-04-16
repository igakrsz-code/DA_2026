# Exercise 1: What Are You Learning?
# Goal: Create a function that displays a message about what you’re learning.

# Key Python Topics:

# Functions (defining and calling)
# print() function

# Step 1: Define a Function
# Define a function named display_message().
# This function should not take any parameters.

# Step 2: Print a Message
# For example: “I am learning about functions in Python.”

# Step 3: Call the Function
# This will execute the code inside the function and print your message.

# Expected Output:

# I am learning about functions in Python.
def display_message():
    """A function that displays a message about what I'm learning."""
    print("I am learning about functions in Python.")
display_message() 

# Exercise 2: What’s Your Favorite Book?
# Goal: Create a function that displays a message about a favorite book.

# Key Python Topics:

# Functions with parameters
# String concatenation or f-strings
# Calling functions with arguments


# Step 1: Define a Function with a Parameter

# Define a function named favorite_book().
# This function should accept one parameter called title.


# Step 2: Print a Message with the Title

# The function needs to output a message like “One of my favorite books is <title>”.



# Step 3: Call the Function with an Argument

# Call the favorite_book() function and provide a book title as an argument.
# For example: favorite_book("Alice in Wonderland").

def favorite_book(title):
    """A function that displays a message about a favorite book."""
    print(f"One of my favorite books is {title}.")  
favorite_book("Alice in Wonderland")

# Exercise 3: Some Geography
# Goal: Create a function that describes a city and its country.

# Key Python Topics:

# Functions with multiple parameters
# Default parameter values
# String formatting


# Step 1: Define a Function with Parameters ok

# Define a function named describe_city().
# This function should accept two parameters: city and country.
# Give the country parameter a default value, such as “Unknown”.


# Step 2: Print a Message

# Inside the function, set up the code to display a sentence like “ is in “.
# Replace <city> and <country> with the parameter values.


# Step 3: Call the Function

# Call the describe_city() function with different city and country combinations.
# Try calling it with and without providing the country argument to see the default value in action.
# Example: describe_city("Reykjavik", "Iceland") and describe_city("Paris").

def describe_city(city, country="Unknown"):
    """A function that describes a city and its country."""
    print(f"{city} is in {country}.")   
describe_city("Reykjavik", "Iceland")
describe_city("Paris")

# Exercise 4: Random
# Goal: Create a function that generates random numbers and compares them.

# Key Python Topics:

# random module
# random.randint() function
# Conditional statements (if, else)


# Step 1: Import the random Module

# At the beginning of your script, use import random to access the random number generation functions.


# Step 2: Define a Function with a Parameter

# Create a function that accepts a number between 1 and 100 as a parameter.


# Step 3: Generate a Random Number

# Inside the function, use random.randint(1, 100) to generate a random integer between 1 and 100.


# Step 4: Compare the Numbers

# If they are the same, print a success message. Otherwise, print a fail message and display both numbers.


# Step 5: Call the Function

# Call the function with a number between 1 and 100.


# Expected Output:

# Success! (if the numbers match)
# Fail! Your number: 50, Random number: 23 (if they don't match)

from pydoc import text
import random
def compare_random_number(user_number):
    """A function that generates a random number and compares it to the user's number."""
    random_number = random.randint(1, 100)
    if user_number == random_number:
        print("Success! Your number matches the random number.")
    else:
        print(f"Fail! Your number: {user_number}, Random number: {random_number}.")
compare_random_number(50)

# Exercise 5 : Create Personalized Shirts

def make_shirt(size = "large", text = "I love Python"):
    """Function to create a personalized shirt."""
    print(f"The size of the shirt is {size} and the text is: '{text}'")
make_shirt()
make_shirt(size = "medium")
make_shirt(size = "small", text = "I like cheese")

# Exercise 6 
magical_names = ["Harry Houdini", "David Copperfield", "Criss Angel"]

def show_magicians(magical_names):
    """Function to show the names of magicians."""
    for name in magical_names:
        print(name)

def make_great(magical_names):
    for i in range(len(magical_names)):
        magical_names[i] = magical_names[i] + " the Great"  

make_great(magical_names)
show_magicians(magical_names)

# Exercise 7
def get_random_temp():
    """Return a random temperature in Celsius."""
    return random.randint(-10, 40)
def main():
    temp = get_random_temp()
    print(f"The temperature right now is {temp} degrees Celsius.")
    if temp < 0:
        print("Brrr, that’s freezing! Wear some extra layers today.")
    elif  0 <= temp <= 16:
        print("Quite chilly! Don’t forget your coat.")
    elif 16 < temp < 23:
        print("Nice weather.")
    elif 23 <= temp < 32:
        print("A bit warm, stay hydrated.")
    else:
        print("It's really hot! Stay cool.")
main()
