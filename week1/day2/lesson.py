my_string = "I love cheese"

fifth_element = my_string[4]
print(fifth_element) # o we start indexing at 0

cheese_list = ["I love cheese"]
print(cheese_list[3]) # IndexError: list index out of range, we only have one element in the list at index 0

my_tuple = (1+3, 2.7, 'Thursday')
print(my_tuple)
print(my_tuple[-2]) # error because in python theres no negative zero

print(my_string[2:6]) 

print(my_string[4:]) # from index 4 to the end of the string
print(my_string[:6]) # from the beginning of the string to index 5

print(my_string[1::2]) # every 2nd character

my_list = [10, 20, 30, 40, 50, 60, 70, 80, 90]

print(my_list[1:6:3]) # from index 1 to index 5, every 3rd element

my_list[1] = "z"
print(my_list) # change the element at index 1 to "z"

my_list.append(100) # add 100 to the end of the list


my_list.remove(100) # remove the first occurrence of 100 from the list
my_list.pop(4) # remove the element at index 4 and return it
my_list.pop() # remove the last element of the list and return it

my_string[3] ="r" # TypeError: 'str' object does not support item assignment, strings are immutable

print(len(my_list)) # 8 - length of the list

print(sum(my_list)) # 350 - sum of the elements in the list

print(sorted(my_list)) # [10, 30, 40, 50, 60, 70, 80, 'z'] - sorted list (note that 'z' is considered greater than numbers

my_list = my_list + [90, 100] # concatenation of lists
print(my_list) # [10, 'z', 30, 40, 50, 60, 70, 80, 90, 100]

my_chars = ['a', 'b', 'c']
print(sorted(my_chars)) # ['a', 'b', 'c'] - sorted list of characters

my_names = ["leeroy", "rubn", "ben zion"]
print(sorted(my_names)) # ['ben zion', 'leeroy', 'rubn'] - sorted list of names (sorted alphabetically

# if one of these names will be in capital letter, it will be sorted before the lowercase names because in ASCII, uppercase letters have lower values than lowercase letters
# so the result will be [Rubn, ben zion, leeroy] if we change "rubn" to "Rubn"

food = ["spam", "eggs", "ham"]
food.append('sushi')
print(food) # ['spam', 'eggs', 'ham', 'sushi'

# exercise 1
list1 =[5,10, 15, 20, 25, 50, 20]
# find the value of 20, if present, replace with 200
# only update the first occurence of a value
list1[list1.index(20)] = 200
print(list1) # [5, 10, 15, 200, 25, 50, 20]

# tuples - ordered, immutable, allows duplicates
a, b, c = my_tuple
print(a) # 4
print(b) # 2.7
print(c) # Thursday

# exercise 2
a_tuple = (10, 20, 30, 40)
a, b, c, d = a_tuple
print(a) # 10
print(b) # 20
print(c) # 30
print(d) # 40

#loops

# for loop
#for <varible_name> in <iterable>:
    # code to execute for each element in the iterable  

fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)
    # output:
    # apple     
    # banana
    # cherry

    print('hi sydney') # this will be printed for each fruit in the list

    for i in range(4, 10):
        print(i) # this will be printed for each fruit in the list, and for each number from 4 to 9
    
    my_range = range(10)
    print(my_range) # range(0, 10) - a range object that represents the numbers from 0 to 9
    print(list(my_range)) # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] - a list of numbers from 0 to 9
    