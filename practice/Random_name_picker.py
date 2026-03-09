import random

names = []

n = int(input("How many names: "))

for i in range(n):
    name = input("Enter name: ")
    names.append(name)

winner = random.choice(names)

print("Selected name:", winner)