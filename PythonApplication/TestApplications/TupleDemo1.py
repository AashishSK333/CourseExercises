# Tuples are ordered and unchangeable/immutable
thistuple = ("apple", 1, 10.5, 1, 'Time', True)

print(thistuple[-1])

print(thistuple[1:5])

print(thistuple.count(1))

print(thistuple.index('Time'))

if "apple" in thistuple:
    print(len(thistuple))

# for modifying a tuple - change tuple into a list & then convert list back to tuple 
list1 = list(thistuple)

list1[1] = "kiwi"
list1.append("Nice")
thistuple = tuple(list1)

print(thistuple)

# add tuple to a tuple
numtuple = (7,8,9)
thistuple += numtuple

for i in range(len(thistuple)):
    print("Tuple value at index {} is: {}\n".format(i+1, thistuple[i]))

