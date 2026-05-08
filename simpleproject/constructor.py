class Person:
    def __init__(self, name, age):  # Constructor
        self.name = name
        self.age = age

    def show_info(self):
        print("Name:", self.name)
        print("Age:", self.age)

# Creating objects (instances)
p1 = Person("Barsha", 20)
p2 = Person("Sita", 22) 
person=Person("ram",20)

# Calling method
p1.show_info()
p2.show_info()
person.show_info()