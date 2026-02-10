# 1
values = [1, 2, 3, 4]
[print(val) for val in values]

# 2
result = [val * 20 for val in [1, 2, 3, 4]]
print(result)

# 3
names= ["Elie", "Tim", "Matt"]
first_letters= [name[0] for name in names]
print(first_letters)

# 4
numbers = [1, 2, 3, 4, 5, 6]
even_numbers = [num for num in numbers if num % 2 == 0]
print(even_numbers)


# 5
numbers1= [1, 2, 3, 4]
numbers2= [3, 4, 5, 6]
print(numbers1.index(3) and numbers2.index(3))

# 6
names = ["Elie", "Tim", "Matt"]
names = [name.lower() for name in names]
print(names)

# 7
string1 = "first"
string2 = "third"

common_letters = []
for ch in string1:
    if ch in string2 and ch not in common_letters:
        common_letters.append(ch)

print(common_letters)

# 8
list_numbers = [12, 24, 36, 48, 60, 72, 84, 96]
divisible_by_12 = [num for num in list_numbers if num % 12 == 0]
print(divisible_by_12)

# 9
word = "amazing"
vowels = "aeiou"
result = [char for char in word if char not in vowels]
print(result)

#10
my_list = [[0, 1, 2] for _ in range(3)]
print(my_list)


#11

my_list = [[i for i in range(10)] for _ in range(10)]
print(my_list)


#1
info = {}
info['name'] = 'Elie'
info['job'] = 'Instructor'
print(info)

#2
abbreviations = ["CA", "NJ", "RI"]
states = ["California", "New Jersey", "Rhode Island"]

state_dict = dict(zip(abbreviations, states))
print(state_dict)

#3
vowels = ['a', 'e', 'i', 'o', 'u']
vowel_dict = {}

for v in vowels:
    vowel_dict[v] = 0

print(vowel_dict)

#4
alphabet = 'abcdefghijklmnopqrstuvwxyz'
alphabet_dict = {}
position = 1  

for letter in alphabet:
    alphabet_dict[position] = letter
    position += 1  

print(alphabet_dict)
