# 🌟 Exercise 4 — Zoo

# class Zoo:
#     def __init__(self, zoo_name):
#         self.name = zoo_name
#         self.animals = []

#     def add_animal(self, new_animal):
#         if new_animal not in self.animals:
#             self.animals.append(new_animal)

#     def get_animals(self):
#         print(self.animals)

#     def sell_animal(self, animal_sold):
#         if animal_sold in self.animals:
#             self.animals.remove(animal_sold)
            

#     def sort_animals(self):
#         groups = {}
#         for animal in sorted(self.animals):

#             letter = animal[0] 
#             if letter not in groups:
#                 groups[letter] = []
#             groups[letter].append(animal)
                   
#         print(groups)




#     def get_groups(self):
#         groups = self.sort_animals()
#         for letter, animals in groups.items():
#             print(f"{letter}: {animals}")
#         print(self.animals)


# Create a zoo and test it
# brooklyn_safari = Zoo("Brooklyn Safari")
# brooklyn_safari.add_animal("Giraffe")
# brooklyn_safari.add_animal("Bear")
# brooklyn_safari.add_animal("Baboon")
# brooklyn_safari.get_animals()
# brooklyn_safari.sell_animal("Bear")
# brooklyn_safari.get_animals()
# brooklyn_safari.get_groups()

class Zoo:
  def __init__(self, zoo_name):
    self.name = zoo_name
    self.animals = [] # a default attribute

  def add_animal(self, new_animal):
    if new_animal not in self.animals:
      self.animals.append(new_animal)

  def get_animals(self):
    print(self.animals)

  def sell_animal(self, animal_sold):
    if animal_sold in self.animals:
      self.animals.remove(animal_sold)

  def sort_animals(self):
    groups = {}

    for animal in sorted(self.animals):
      letter = animal[0] # takes the first character
      #'A'?'B?'

      if letter not in groups:
        groups[letter] = [] # 'B': []

      groups[letter].append(animal)

    return groups

  def get_groups(self):
      groups = self.sort_animals()
      for letter, animals in groups.items(): #'B', ['Baboon', 'Bear'...]
        print(f"{letter}: {animals}")

# Create a zoo and test it
brooklyn_safari = Zoo("Brooklyn Safari")
brooklyn_safari.add_animal("Giraffe")
brooklyn_safari.add_animal("Bear")
brooklyn_safari.add_animal("Baboon")
brooklyn_safari.get_animals()
brooklyn_safari.sell_animal("Bear")
brooklyn_safari.get_animals()
brooklyn_safari.get_groups()

