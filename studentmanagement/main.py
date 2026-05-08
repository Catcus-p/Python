from student import add_student, view_students, search_student, delete_student


def menu():
    print("\n===== STUDENT SYSTEM =====")
    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Delete Student")
    print("5. Exit")


while True:
    menu()
    choice = input("Enter choice: ")

    if choice == "1":
        name = input("Name: ")
        age = input("Age: ")
        course = input("Course: ")
        add_student(name, age, course)
        print("Student added successfully ✔")

    elif choice == "2":
        students = view_students()
        for s in students:
            print(s)

    elif choice == "3":
        name = input("Enter name to search: ")
        results = search_student(name)
        print(results)

    elif choice == "4":
        student_id = int(input("Enter ID to delete: "))
        delete_student(student_id)
        print("Deleted successfully ✔")

    elif choice == "5":
        print("Exiting...")
        break

    else:
        print("Invalid choice ❌")