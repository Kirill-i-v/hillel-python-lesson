COMMANDS = ("show", "add", "quit", "retrieve")

students = [
    {"id": 1,
     "name": "John Smith",
     "marks": [4, 2, 3, 4, 5, 2],
     "info": "John is..."},
    {"id": 2,
     "name": "Marry White",
     "marks": [3, 5, 3, 4, 5, 3],
     "info": "Marry is..."},
]


def find_student(id_: int):
    for student in students:
        if student['id'] == id_:
            return student

    return None


def show_students():
    print("=" * 30)

    print("This is a list of students")

    for student in students:
        print(f"{student['id']}. {student['name']}. Marks: {student['marks']}")

    print("=" * 30)


def show_student(id_: int):
    student: dict = find_student(id_)

    if not student:
        print(f"There is no student with id {id_}")
        return

    print("Detailed about student:\n")

    print(f"{student['id']}. {student['name']}. Marks: {student['marks']}\n"
          f"Details: {student['info']}")


def add_student(student_name: str, details: str | None):
    new_id = len(students) + 1
    if details.strip() == "":
        details = None
    instance = {"id": new_id, "name": student_name, "marks": [], "info": details}
    students.append(instance)
    return


def main():
    print(f"Welcome to the Digital Journal.\nAvailable commands: {COMMANDS}")
    while True:
        user_input = input("Enter the command: ")

        if user_input not in COMMANDS:
            print(f"Command {user_input} is not available.\n")
            continue
        if user_input == "quit":
            print("See you next time.")
            break
        try:
            if user_input == "show":
                show_students()
            elif user_input == "retrieve":
                id_ = input("Enter student's id that you are looking for: ")
                show_student(int(id_))
            elif user_input == "add":
                name = input("Enter student's name:")
                details = input("Enter student's details or press 'Enter' to skip:")
                add_student(name, details)
        except ValueError:
            print("Invalid input details")
        except Exception as e:
            print(e)


main()
