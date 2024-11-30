#def add_1(x,y):
#    return x+y

add_1 = lambda x,y: x+y

result = add_1(10, 14)

print(result)

# Lambda function is used inside another functions like map & filter
# The map() function executes a specified function for each item in an iterable.
# The item is sent to the function as a parameter.
number_list = [1,2,3,4,5,6,7,8,9,10]

#def square(x):
#    return x**2

#square = lambda x: x**2

#squares = list(map(square, number_list))

squares = list(map(lambda x:x**2, number_list))
print(squares)

# filter function

#evenfunction = lambda x: x%2==0

filter_even = list(filter(lambda x: x%2==0, number_list))
print(filter_even)