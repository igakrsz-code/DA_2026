#Exercise 1: Favorite Numbers
#Key Python Topics:
#Sets
#Adding/removing items in a set
#Set concatenation (using union)
#Instructions:
#Create a set called my_fav_numbers and populate it with your favorite numbers.
#Add two new numbers to the set.
#Remove the last number you added to the set.
#Create another set called friend_fav_numbers and populate it with your friend’s favorite numbers.
#Concatenate my_fav_numbers and friend_fav_numbers to create a new set called our_fav_numbers.
#Note: Sets are unordered collections, so ensure no duplicate numbers are added.

my_fav_numbers = {3, 7, 42}
my_fav_numbers.add(10)
my_fav_numbers.add(15)
my_fav_numbers.remove(15)
friend_fav_numbers = {5, 10, 20}
our_fav_numbers = my_fav_numbers.union(friend_fav_numbers)
print(our_fav_numbers) 

#Exercise 2: Tuple
#Key Python Topics:
#Tuples (immutability)
#Instructions:
#Given a tuple of integers, try to add more integers to the tuple.
#Hint: Tuples are immutable, meaning they cannot be changed after creation. Think about why you can’t add more integers to a tuple.
 
my_tuple = (1, 2, 3)
# Attempting to add more integers to the tuple will result in an error
new_tuple = my_tuple + (4, 5) # This creates a new tuple that combines the original tuple with the new integers
print(new_tuple) # (1, 2, 3, 4, 5)

# Exercise 3: List Manipulation
#Key Python Topics:
#Lists
#List methods: append, remove, insert, count, clear
#Instructions:

#You have a list: basket = ["Banana", "Apples", "Oranges", "Blueberries"]
#Remove "Banana" from the list.
#Remove "Blueberries" from the list.
#Add "Kiwi" to the end of the list.
#Add "Apples" to the beginning of the list.
#Count how many times "Apples" appear in the list.
#Empty the list.
#Print the final state of the list.
basket = ["Banana", "Apples", "Oranges", "Blueberries"]
basket.remove("Banana")
basket.remove("Blueberries")
basket.append("Kiwi")
basket.insert(0, "Apples")
print(basket.count("Apples")) # 2
basket.clear()
print(basket) 

# Exercise 4: Floats
#Key Python Topics:
#Lists
#Floats and integers
#Range generation

#Instructions:

#Recap: What is a float? What’s the difference between a float and an integer?
#Create a list containing the following sequence of mixed types: floats and integers:
#1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5.

#Avoid hard-coding each number manually.
my_list = [x * 0.5 for x in range(3, 11)] 

#Exercise 5: For Loop
#Key Python Topics:

#Loops (for)
#Range and indexing


#Instructions:

#Write a for loop to print all numbers from 1 to 20, inclusive.
#Write another for loop that prints every number from 1 to 20 where the index is even.
for i in range(1, 21):
    print(i)
for i in range(1, 21):
    if i % 2 == 0:
        print(i)


# Exercise 6: While Loop
#Instructions:

#Use an input to ask the user to enter their name.
#Using a while True loop, check if the user gave a proper name (not digits and at least 3 letters long)
#hint: check for the method isdigit()
#if the input is incorrect, keep asking for the correct input until it is correct
#if the input is correct print “thank you” and break the loop
while True:
    name = input("Please enter your name: ")
    if name.isdigit() or len(name) < 3:
        print("Invalid input. Please enter a proper name.")
    else:
        print("Thank you!")
        break

# Exercise 7: Favorite Fruits
#Instructions:
#Instructions:

#Ask the user to input their favorite fruits (they can input several fruits, separated by spaces).
#Store these fruits in a list.
#Ask the user to input the name of any fruit.
#If the fruit is in their list of favorite fruits, print:
#"You chose one of your favorite fruits! Enjoy!"
#If not, print:
#"You chose a new fruit. I hope you enjoy it!"

favorite_fruits = input("Please enter your favorite fruits (separated by spaces): ").split()
fruit = input("Please enter the name of any fruit: ")
if fruit in favorite_fruits:
    print("You chose one of your favorite fruits! Enjoy!")
else:
    print("You chose a new fruit. I hope you enjoy it!")

#Exercise 8: Pizza Toppings

#Instructions:

#Write a loop that asks the user to enter pizza toppings one by one.
#Stop the loop when the user types 'quit'.
#For each topping entered, print:
#"Adding [topping] to your pizza."
##After exiting the loop, print all the toppings and the total cost of the pizza.
#The base price is $10, and each topping adds $2.50.

toppings = []
while True:
    topping = input("Enter a pizza topping (or type 'quit' to finish): ")
    if topping.lower() == 'quit':
        break
    toppings.append(topping)
    print(f"Adding {topping} to your pizza.")

print(f"Toppings added: {', '.join(toppings)}")
total_cost = 10 + len(toppings) * 2.5
print(f"Total cost of the pizza: ${total_cost:.2f}")

#Exercise 9: Cinemax Tickets


#Instructions:

#Ask for the age of each person in a family who wants to buy a movie ticket.
#Calculate the total cost based on the following rules:
#Free for people under 3.
#$10 for people aged 3 to 12.
#$15 for anyone over 12.
#Print the total ticket cost.
total_cost = 0
while True:
    age_input = input("Enter the age of a family member (or type 'done' to finish): ")
    if age_input.lower() == 'done':
        break
    age = int(age_input)
    if age < 3:
        cost = 0
    elif 3 <= age <= 12:
        cost = 10
    else:
        cost = 15
    total_cost += cost
print(f"Total ticket cost: ${total_cost}")
