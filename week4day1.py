import numpy as np

# exercise 1 : Array Creation and Manipulation
arr1 = np.arange(10)

# exercise 2 : Type Conversion and Array Operations
arr2 = np.array([3.14, 2.17, 0, 1, 2]).astype(int)

# exercise 3 : Working with Multi-Dimensional Arrays
arr3 = np.arange(1, 10).reshape(3, 3)

# exercise 4 : Creating Multi-Dimensional Array with Random Numbers
np.random.seed(42)
arr4 = np.random.random((4, 5))

# exercise 5 : Indexing Arrays
array5 = np.array([[21, 22, 23, 22, 22],
                   [20, 21, 22, 23, 24],
                   [21, 22, 23, 22, 22]])
second_row = array5[1]

# exercise 6 : Reversing elements
arr6 = np.arange(10)[::-1]

# exercise 7 : Identity Matrix
arr7 = np.eye(4)

# exercise 8 : Simple Aggregate Funcs
arr8 = np.arange(1, 10)
sum_arr8 = np.sum(arr8)
avg_arr8 = np.mean(arr8)

# exercise 9 : Create Array and Change its Structure
arr9 = np.arange(1, 21).reshape(4, 5)

# exercise 10 : Conditional Selection of Values
arr10 = np.arange(10)
odd_values = arr10[arr10 % 2 == 1]
