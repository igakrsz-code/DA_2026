# =========================================
# CHALLENGE 1: SORTING WORDS
# =========================================

# Step 1: Get input from the user
words_input = input("Enter words separated by commas: ")

# Step 2: Split the string into a list
words_list = words_input.split(",")

# Step 3: Sort the list alphabetically
words_list.sort()

# Step 4: Join the sorted list back into a string
sorted_words = ",".join(words_list)

# Step 5: Print the result
print("Sorted words:", sorted_words)


# =========================================
# CHALLENGE 2: LONGEST WORD
# =========================================

def longest_word(sentence):
    # Step 2: Split the sentence into words
    words = sentence.split()

    # Step 3: Initialize variables
    longest = ""

    # Step 4: Iterate through the words
    for word in words:
        # Step 5: Compare word lengths
        if len(word) > len(longest):
            longest = word

    # Step 6: Return the longest word
    return longest


# =========================================
# Example tests
# =========================================

print(longest_word("Margaret's toy is a pretty doll."))
print(longest_word("A thing of beauty is a joy forever."))
print(longest_word("Forgetfulness is by all means powerless!"))
