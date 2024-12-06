class Person:
    def __init__(self, name, age) -> None:
        self.name = name
        self.age = age

p1 = Person("Jack", 36)

print(p1.name)
print(p1.age)