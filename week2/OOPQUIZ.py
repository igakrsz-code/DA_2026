
# EXERCISE 1

# 1. What is a class?
# A class is a blueprint used to create objects. It defines the attributes (data)
# and methods (functions) that the objects created from it will have.

# 2. What is an instance?
# An instance is an object created from a class.
# Example: if Car is a class, then my_car = Car() is an instance.

# 3. What is encapsulation?
# Encapsulation is the practice of bundling data and the methods that operate
# on that data inside a class, and restricting direct access to some of the data.

# 4. What is abstraction?
# Abstraction means hiding complex implementation details and exposing only
# the necessary parts of an object.

# 5. What is inheritance?
# Inheritance allows a class to inherit properties and methods from another class.

# 6. What is multiple inheritance?
# Multiple inheritance means a class can inherit from more than one parent class.

# 7. What is polymorphism?
# Polymorphism allows the same method name to behave differently depending on
# the object that calls it.

# 8. What is Method Resolution Order (MRO)?
# MRO is the order Python follows when searching for a method in a class hierarchy,
# especially when multiple inheritance is involved.


# =========================================
# EXERCISE 2: DECK OF CARDS
# =========================================

import random


# Card class
class Card:

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f"{self.value} of {self.suit}"


# Deck class
class Deck:

    def __init__(self):
        self.cards = []
        self.shuffle()

    def shuffle(self):
        """
        Create a full deck of 52 cards and shuffle them.
        """

        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        values = ["A", "2", "3", "4", "5", "6", "7",
                  "8", "9", "10", "J", "Q", "K"]

        self.cards = []

        for suit in suits:
            for value in values:
                self.cards.append(Card(suit, value))

        random.shuffle(self.cards)

    def deal(self):
        """
        Deal one card from the deck and remove it from the deck.
        """

        if len(self.cards) == 0:
            return None

        return self.cards.pop()
