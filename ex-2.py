# 1
values= [1, 2, 3, 4]
for val in values :
    print(val)
# 2
values= [1, 2, 3, 4]
print(values * 20)

# 3
names= ["Elie", "Tim", "Matt"]
first_letters= [name[0] for name in names]
print(first_letters)

# 4
numbers=[1, 2, 3, 4, 5, 6]
print(numbers[ 1: : 2])

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
list = [[0, 1, 2]] * 3
print(list)

#11

list = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]] * 10
print(list)
