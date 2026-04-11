# # Exercise 1: Cats
# # The Cat class has already been written for you. Your job is to:

# # Create three Cat objects with different names and ages
# # Write a function find_oldest_cat that takes three Cat objects and returns the oldest one
# # Print the result as: "The oldest cat is <name>, and is <age> years old."
# # class Cat:
# #     def __init__(self, cat_name, cat_age):
# #         self.name = cat_name
# #         self.age  = cat_age
# # Hint: compare .age attributes to find the maximum.

# # 🌟 Exercise 1 — Cats

# class Cat:
#     def __init__(self, cat_name, cat_age):
#         self.name = cat_name
#         self.age  = cat_age


# cat1 = Cat("Nacha", 3)
# cat2 = Cat("Benji", 4)
# cat3 = Cat("Pushkin", 5)


# def find_oldest_cat(cat1, cat2, cat3):
#     oldest = cat1

#     if cat2.age > oldest.age:
#         oldest = cat2

#     if cat3.age > oldest.age:
#         oldest = cat3

#     return oldest


# oldest = find_oldest_cat(cat1, cat2, cat3)

# print(f"The oldest cat is {oldest.name}, and is {oldest.age} years old.")


### 🌟 Exercise 2: Dogs

# Now it's your turn to build the `Dog` class **from scratch**.

# **Step 1 — Create the Dog class:**
# - `__init__` takes `name` and `height` as parameters
# - `bark()` prints `"<name> goes woof!"`
# - `jump()` prints `"<name> jumps <height*2> cm high!"`

# **Step 2 — Create two dog objects:**
# - `davids_dog` with name `"Rex"` and height `50`
# - `sarahs_dog` with name `"Bella"` and height `35`

# **Step 3 — Print details and call methods** for each dog

# **Step 4 — Compare their sizes** and print which is bigger

# 🌟 Exercise 2 — Dogs

# Step 1 — Create the Dog class
class Dog:
    def __init__(self, name, height):
        self.name = name
        self.height = height

    def bark(self):
        print(f"{self.name} goes woof!")

    def jump(self):
        print(f"{self.name} jumps {self.height * 2} cm high!")


# Step 2 — Create dog objects
davids_dog = Dog("Rex", 50)
sarahs_dog = Dog("Bella", 35)


# # Step 3 — Print details and call methods
# print(davids_dog.name, davids_dog.height)
# davids_dog.bark()
# davids_dog.jump()

# print(sarahs_dog.name, sarahs_dog.height)
# sarahs_dog.bark()
# sarahs_dog.jump()


# # Step 4 — Compare their sizes
# if davids_dog.height > sarahs_dog.height:
#     print(f"{davids_dog.name} is bigger")
# elif sarahs_dog.height > davids_dog.height:
#     print(f"{sarahs_dog.name} is bigger")
# else:
#     print("They are the same size")

#  Exercise 3: Who's the Song Producer?
# Build a Song class:

# __init__ takes lyrics (a list of strings)
# sing_me_a_song() prints each lyric line on a new line
# Then create a song of your choice and call sing_me_a_song().

# Example output:

# There's a lady who's sure
# all that glitters is gold
# and she's buying a stairway to heaven
# # 🌟 Exercise 3 — Song

# class Song:
#     def __init__(self, lyrics):
#         pass  # store lyrics as attribute

#     def sing_me_a_song(self):
#         pass  # print each line

# # Create a song and call sing_me_a_song()
# [ ]


class Song:
    def __init__(self, lyrics):
        self.lyrics = lyrics

    def sing_me_a_song(self):
        for line in self.lyrics:
            print(line)

stairway = Song([
    "There's a lady who's sure",
    "all that glitters is gold",
    "and she's buying a stairway to heaven"
])

stairway.sing_me_a_song()