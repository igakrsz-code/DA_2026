# Challenge 1: Letter Index Dictionary
# Goal: Create a dictionary that stores the indices (number of the position) of each letter in a word provided by the user(input()).



# Instructions:
# 1. User Input:

# Ask the user to enter a word.
# Store the input word in a variable.
# 2. Creating the Dictionary:

# Iterate through each character of the input word using a loop.
# And check if the character is already a key in the dictionary.

#     * If it is, append the current index to the list associated with that key.
#     * If it is not, create a new key-value pair in the dictionary.
# Ensure that the characters (keys) are strings.
# Ensure that the indices (values) are stored in lists.
# 3. Expected Output:

# For the input “dodo”, the output should be: {"d": [0, 2], "o": [1, 3]}.
# For the input “froggy”, the output should be: {"f": [0], "r": [1], "o": [2], "g": [3, 4], "y": [5]}.
# For the input “grapes”, the output should be: {"g": [0], "r": [1], "a": [2], "p": [3], "e": [4], "s": [5]}.


user_word = input("Enter a word: ")
letter_index_dict = {}
for index, letter in enumerate(user_word):
    if letter in letter_index_dict:
        letter_index_dict[letter].append(index)
    else:
        letter_index_dict[letter] = [index]
print(letter_index_dict)

# Instructions:
#1. Store Data:

# You will be provided with a dictionary (items_purchase) where the keys are the item names and the values are their prices (as strings with a dollar sign). The priority is defined by the position of the iten on the dictionary: from the most important to the less important.
# You will also be given a string (wallet) representing the amount of money you have.
# 2. Data Cleaning:

# You need to clean the dollar sign and the commas using python. Don’t hard code it.
# 3. Determining Affordable Items:

# create a list called basket and add there the items that you can buy with the money you have on the wallet
# Don’t forget to update the wallet after buying an item.
# If the basket is empty (no items can be afforded), return the string “Nothing”.
# Otherwise, print the basket list in alphabetical order.
items_purchase = {
    "laptop": "$999.99",
    "headphones": "$199.99",
    "mouse": "$49.99",
    "keyboard": "$89.99",
    "monitor": "$299.99"
}
wallet = "$1500.00"

cleaned_items = {item: float(price.replace("$", "").replace(",", "")) for item, price in items_purchase.items()}
cleaned_wallet = float(wallet.replace("$", "").replace(",", ""))

basket = []
for item, price in cleaned_items.items():
    if price <= cleaned_wallet:
        basket.append(item)
        cleaned_wallet -= price
if not basket:
    print("Nothing")
else:
    print(sorted(basket))
