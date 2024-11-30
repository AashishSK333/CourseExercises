values = [(1, 'b', "hello"), (2, 'a', "world"), (3, 'c', "great")]
# sort the above list which is constituting of multiple tuples on index 1 element
sorted_values=sorted(values, key=lambda x:x[1])

print(sorted_values)