# Step 1 — Base class Pet
class Pet:
    is_lazy = False   # class attribute

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def description(self):
        print(f"{self.name} is {self.age} years old.")

    def make_sound(self):
        print("...")


# Step 2 — Child class Cat
class Cat(Pet):
    is_lazy = True   # override class attribute

    def __init__(self, name, age, indoor: bool):
        super().__init__(name, age)   # call parent constructor
        self.indoor = indoor

    def make_sound(self):
        print(f"{self.name} says: Meow!")


# Step 3 — Child class Dog
class Dog(Pet):
    def __init__(self, name, age, breed: str):
        super().__init__(name, age)
        self.breed = breed

    def make_sound(self):
        print(f"{self.name} says: Woof!")

    def fetch(self, item):
        print(f"{self.name} fetches the {item}!")


# Step 4 — Test it
cat = Cat("Whiskers", 4, indoor=True)
dog = Dog("Buddy", 2, "Beagle")

cat.description()     # from Pet
cat.make_sound()      # Cat's version
dog.make_sound()      # Dog's version
dog.fetch("ball")

print(Cat.is_lazy)    # True
print(Dog.is_lazy)    # False (inherited from Pet)