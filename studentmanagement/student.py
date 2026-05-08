import json

FILE_NAME = "database.txt"


def load_data():
    try:
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    except:
        return []


def save_data(data):
    with open(FILE_NAME, "w") as f:
        json.dump(data, f, indent=4)


def add_student(name, age, course):
    data = load_data()
    student = {
        "id": len(data) + 1,
        "name": name,
        "age": age,
        "course": course
    }
    data.append(student)
    save_data(data)


def view_students():
    return load_data()


def search_student(name):
    data = load_data()
    return [s for s in data if name.lower() in s["name"].lower()]


def delete_student(student_id):
    data = load_data()
    new_data = [s for s in data if s["id"] != student_id]
    save_data(new_data)