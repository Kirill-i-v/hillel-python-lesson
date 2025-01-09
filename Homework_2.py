students = {
    1: {
        "name": "John Doe",
        "marks": [4, 5, 1, 4, 5, 2, 5],
        "info": "John is 22 y.o. Hobbies: music",
    },
    2: {
        "name": "Marry Black",
        "marks": [4, 1, 3, 4, 5, 1, 2, 2],
        "info": "Marry is 23 y.o. Hobbies: football",
    },
}

LAST_ID_CONTEXT = 2


def represent_students():
    for id_, student in students.items():
        print(f"[{id_}] {student['name']}, marks: {student['marks']}")


def add_student(student: dict) -> dict | None:
    global LAST_ID_CONTEXT

    if len(student) != 2:
        return None
    elif not student.get("name") or not student.get("marks"):
        return None
    else:
        LAST_ID_CONTEXT += 1
        students[LAST_ID_CONTEXT] = student

    return student


def search_student(id_: int) -> dict | None:
    return students.get(id_)


def delete_student(id_: int):
    if search_student(id_):
        del students[id_]
        print(f"Student with id '{id_}' is deleted")
    else:
        print(f"There is no student with id '{id_}' in the storage")


def update_student(id_: int, payload: dict) -> dict:
    students[id_] = payload
    return payload


def student_details(student: dict) -> None:
    print(f"Detailed info: [{student['name']}] - Marks: {student['marks']}")


def parse(data: str) -> tuple[str, list[int]]:

    template = "John Doe;4,5,4,5,4,5"

    items = data.split(";")

    if len(items) != 2:
        raise Exception(f"Incorrect data. Template: {template}")

    name, raw_marks = items

    try:
        marks = [int(item) for item in raw_marks.split(",")]
    except ValueError as error:
        print(error)
        raise Exception(f"Marks are incorrect. Template: {template}") from error

    return name, marks


def ask_student_payload():

    prompt = "Enter student's payload using the following template:\n'John Doe;4,5,4,5,4,5': "

    if not (payload := parse(input(prompt))):
        return None
    else:
        name, marks = payload

    return {"name": name, "marks": marks}


def handle_management_command(command: str):
    if command == "show":
        represent_students()

    elif command == "retrieve":
        search_id = input("Enter student's ID to retrieve: ")

        try:
            id_ = int(search_id)
        except ValueError as error:
            raise Exception(f"ID '{search_id}' is not a valid value") from error
        else:
            if student := search_student(id_):
                student_details(student)
            else:
                print(f"There is no student with ID: '{id_}'")

    elif command == "remove":
        delete_id = input("Enter student's ID to remove: ")

        try:
            id_ = int(delete_id)
        except ValueError as error:
            raise Exception(f"ID '{delete_id}' is not a valid value") from error
        else:
            delete_student(id_)

    elif command == "change":
        update_id = input("Enter student's ID you want to change: ")

        try:
            id_ = int(update_id)
        except ValueError as error:
            raise Exception(f"ID '{update_id}' is not a valid value") from error
        else:
            if data := ask_student_payload():
                update_student(id_, data)
                print(f"✅ Student is updated")
                if student := search_student(id_):
                    student_details(student)
                else:
                    print(f"❌ Cannot change user with data {data}")

    elif command == "add":
        data = ask_student_payload()
        if data is None:
            return None
        else:
            if not (student := add_student(data)):
                print(f"❌ Can't create user with data: {data}")
            else:
                print(f"✅ New student '{student['name']}' is created")

    elif command == "add_mark":
        student_id = input("Enter student's ID to add a mark: ")

        try:
            id_ = int(student_id)
        except ValueError as error:
            raise Exception(f"ID '{student_id}' is not a valid value") from error
        else:
            if student := search_student(id_):
                new_mark = input(f"Enter the new mark for {student['name']}: ")
                try:
                    mark = int(new_mark)
                    student['marks'].append(mark)
                    print(f"✅ Mark added to {student['name']}. Updated marks: {student['marks']}")
                except ValueError:
                    print("❌ Invalid mark. Please enter a numeric value.")
            else:
                print(f"There is no student with ID: '{id_}'")

    elif command == "partial_update":
        update_id = input("Enter student's ID for partial update: ")

        try:
            id_ = int(update_id)
        except ValueError as error:
            raise Exception(f"ID '{update_id}' is not a valid value") from error
        else:
            if student := search_student(id_):
                print(f"Updating student {student['name']}")
                name_input = input(f"Enter new name (or leave blank to keep '{student['name']}'): ")
                marks_input = input(f"Enter new marks (comma separated, or leave blank to keep {student['marks']}): ")

                if name_input:
                    student['name'] = name_input
                if marks_input:
                    try:
                        student['marks'] = [int(x) for x in marks_input.split(',')]
                    except ValueError:
                        print("❌ Invalid marks input. Please use numeric values separated by commas.")
                        return

                update_student(id_, student)
                print(f"✅ Student data updated: {student}")
            else:
                print(f"There is no student with ID: '{id_}'")

    else:
        raise SystemExit(f"Unrecognized command: '{command}'")


def handle_user_input():

    system_commands = ("quit", "help")
    management_commands = ("show", "add", "retrieve", "remove", "change", "add_mark", "partial_update")
    available_commands = system_commands + management_commands

    help_message = (
        "Welcome to the Journal application. Use the menu to interact with the application.\n"
        f"Available commands: {available_commands}"
    )

    print(help_message)

    while True:
        command = input("Enter the command: ")

        if command == "quit":
            print(f"\nThanks for using Journal application. Bye!")
            break
        elif command == "help":
            print(help_message)
        elif command in management_commands:
            handle_management_command(command=command)
        else:
            print(f"Unrecognized command '{command}'")


handle_user_input()
