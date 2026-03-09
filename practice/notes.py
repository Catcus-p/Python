note = input("Write your note: ")

with open("notes.txt", "a") as file:
    file.write(note + "\n")

print("Note saved!")

with open("notes.txt", "r") as file:
    content = file.read()

print("Your Notes:")
print(content)