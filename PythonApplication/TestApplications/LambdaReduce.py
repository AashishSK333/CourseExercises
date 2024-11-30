from functools import reduce

numbers = [1,3,5,6]

# using reduce to sum the list without initializer
sum_of_numbers = reduce(lambda acc, x: acc+x, numbers)
print(sum_of_numbers)

# using reduce to find the maximum value from the list
max_of_numbers = reduce(lambda acc, x: acc if acc > x else x, numbers)
print(max_of_numbers)