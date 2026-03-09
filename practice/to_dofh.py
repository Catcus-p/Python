while True:
    print("\n1. Add Task")
    print("2. View Tasks")
    print("3. Exit")

    choice = input("Choose: ")

    if choice == "1":
        task = input("Enter task: ")
        with open("tasks.txt", "a") as file:
            file.write(task + "\n")

    elif choice == "2":
        with open("tasks.txt", "r") as file:
            print("\nTasks:")
            print(file.read())

    elif choice == "3":
        break