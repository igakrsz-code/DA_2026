# Exercise 1: Random Sentence Generator (~20 minutes)
# Build a program that reads words from a file and generates random sentences.

# Functions to implement:

# Function	Details
# get_words_from_file(file_path)	Opens the file, reads content, splits into words, returns the list
# get_random_sentence(length)	Takes a number, picks that many random words, joins with spaces, returns lowercase string
# main()	Asks for sentence length (2-20), validates input with try/except, calls the other functions
# Rules:

# main() should ask the user for a number between 2 and 20 (inclusive)
# If the user types something that isn't a number → catch ValueError, print error message
# If the number is outside 2-20 → print an error message (not an exception — just a check)
# Use random.choice() to pick random words
# The sentence should be all lowercase
# Example output:

# Enter sentence length (2-20): 5
# Generated sentence: gentle river apple swift code

# Enter sentence length (2-20): hello
# Invalid input! Please enter a number.

# Enter sentence length (2-20): 25
# Please enter a number between 2 and 20.


#template of code

# def get_number():
#     user_input = "hello"  # simulate bad input
#     try:
#         number = int(user_input)
#         print(f"You entered: {number}")
#     except ValueError:
#         print(f"'{user_input}' is not a valid number!")


# get_number()


# def get_number_good():
#     user_input = "42"  # simulate good input
#     try:
#         number = int(user_input)
#         print(f"You entered: {number}")
#     except ValueError:
#         print(f"'{user_input}' is not a valid number!")


# get_number_good()

import random

def get_words_from_file(file_path):
    with open(file_path, "r") as f:
        content = f.read()
    return content.split()


def get_random_sentence(length):
    words = get_words_from_file("words.txt")
    chosen = [random.choice(words) for _ in range(length)]
    return " ".join(chosen).lower()


def main():
    try:
        length = int(input("Enter sentence length (2-20): "))
        if length < 2 or length > 20:
            print("Please enter a number between 2 and 20.")
            return
    except ValueError:
        print("Invalid input! Please enter a number.")
        return  # <- stop if input is bad

    sentence = get_random_sentence(length)
    print(f"Generated sentence: {sentence}")
main()

