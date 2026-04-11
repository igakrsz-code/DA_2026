
# 🌟 Exercise 1: Pets


class Pets:
    def __init__(self, animals):
        self.animals = animals

    def walk(self):
        for animal in self.animals:
            print(animal.walk())

class Cat:
    is_lazy = True

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def walk(self):
        return f'{self.name} is just walking around'

class Bengal(Cat):
    def sing(self, sounds):
        return f'{sounds}'

class Chartreux(Cat):
    def sing(self, sounds):
        return f'{sounds}'

class Siamese(Cat):
    pass  # Siamese breed inherits from Cat


bengal = Bengal("Leo", 3)
chartreux = Chartreux("Misty", 2)
siamese = Siamese("Luna", 1)
all_cats = [bengal, chartreux, siamese]


sara_pets = Pets(all_cats)

print("=== Pets Exercise ===")
sara_pets.walk()
print("\n")


# 🌟 Exercise 2: Dogs


class Dog:
    def __init__(self, name, age, weight):
        self.name = name
        self.age = age
        self.weight = weight

    def bark(self):
        return f"{self.name} is barking"

    def run_speed(self):
        return self.weight / self.age * 10

    def fight(self, other_dog):
        self_power = self.run_speed() * self.weight
        other_power = other_dog.run_speed() * other_dog.weight
        if self_power > other_power:
            return f"{self.name} wins!"
        elif self_power < other_power:
            return f"{other_dog.name} wins!"
        else:
            return "It's a tie!"


dog1 = Dog("Rex", 4, 20)
dog2 = Dog("Buddy", 3, 15)
dog3 = Dog("Max", 5, 25)

print("=== Dogs Exercise ===")
print(dog1.bark())
print(f"{dog2.name} run speed: {dog2.run_speed()}")
print(dog1.fight(dog2))
print("\n")


# 🌟 Exercise 3: PetDog


import random

class PetDog(Dog):
    def __init__(self, name, age, weight):
        super().__init__(name, age, weight)
        self.trained = False

    def train(self):
        print(self.bark())
        self.trained = True

    def play(self, *args):
        names = ", ".join([dog.name if isinstance(dog, Dog) else dog for dog in args])
        print(f"{self.name} and {names} all play together")

    def do_a_trick(self):
        if self.trained:
            tricks = ["does a barrel roll", "stands on his back legs", "shakes your hand", "plays dead"]
            print(f"{self.name} {random.choice(tricks)}")


pet1 = PetDog("Fido", 2, 10)
pet2 = PetDog("Buddy", 3, 12)

print("=== PetDog Exercise ===")
pet1.train()
pet1.play(pet2)
pet1.do_a_trick()
print("\n")


# 🌟 Exercise 4: Family and Person Classes


class Person:
    def __init__(self, first_name, age):
        self.first_name = first_name
        self.age = age
        self.last_name = ""

    def is_18(self):
        return self.age >= 18

class Family:
    def __init__(self, last_name):
        self.last_name = last_name
        self.members = []

    def born(self, first_name, age):
        new_person = Person(first_name, age)
        new_person.last_name = self.last_name
        self.members.append(new_person)

    def check_majority(self, first_name):
        person = next((m for m in self.members if m.first_name == first_name), None)
        if person:
            if person.is_18():
                print(f"You are over 18, your parents Jane and John accept that you will go out with your friends")
            else:
                print("Sorry, you are not allowed to go out with your friends.")

    def family_presentation(self):
        print(f"Family Last Name: {self.last_name}")
        for member in self.members:
            print(f"{member.first_name}, Age: {member.age}")


my_family = Family("Smith")
my_family.born("Alice", 20)
my_family.born("Tom", 16)

print("=== Family Exercise ===")
my_family.check_majority("Alice")
my_family.check_majority("Tom")
my_family.family_presentation()
