greetings = "Hello, World!"
print(type(greetings))
print(type('hi'))
print(type(123))
print(type("123"))

#string method
print(greetings.upper())
print(greetings.lower())
print(len(greetings))

# string concatentation - joining two strings together
first_name = "John"
last_name = "Doe"
full_name = first_name + " " + last_name
print(full_name)

print(' Ha ' * 3) # string repetition - hahaha

test = "   Hello, World!   "
print(test.replace("world", "Python")) # string replacement
print(test.count("l"))




