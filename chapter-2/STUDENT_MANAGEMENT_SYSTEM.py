import json
import shutil
from pathlib import Path

FILE_PATH = Path("students.json")
BACKUP_PATH = Path("students_backup.json")


def load_students():
    if not FILE_PATH.exists():
        return {}
    try:
        with open(FILE_PATH, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, PermissionError):
        return {}


def save_students(data):
    with open(FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)


def create_backup():
    if FILE_PATH.exists():
        shutil.copy(FILE_PATH, BACKUP_PATH)


def validate_input(student_id, name, department, semester):
    if not student_id or not str(student_id).strip():
        return False
    if not name or not name.strip():
        return False
    if not department or not department.strip():
        return False
    if not semester or not str(semester).strip():
        return False
    return True


def add_student(student_id, name, department, semester):
    if not validate_input(student_id, name, department, semester):
        print("Error: Invalid or missing fields.")
        return False
    data = load_students()
    if student_id in data:
        print("Error: Student ID already exists.")
        return False
    data[student_id] = {
        "name": name,
        "department": department,
        "semester": semester,
    }
    save_students(data)
    print("Student added successfully.")
    return True


def list_students():
    data = load_students()
    if not data:
        print("No student records found.")
        return
    for sid, info in data.items():
        print(
            f"ID: {sid} | Name: {info['name']} | Dept: {info['department']} | Semester: {info['semester']}"
        )


def search_student(student_id):
    data = load_students()
    if student_id in data:
        info = data[student_id]
        print(
            f"Found - ID: {student_id} | Name: {info['name']} | Dept: {info['department']} | Semester: {info['semester']}"
        )
        return info
    print("Student not found.")
    return None


def update_student(student_id, name, department, semester):
    if not validate_input(student_id, name, department, semester):
        print("Error: Invalid or missing fields.")
        return False
    data = load_students()
    if student_id not in data:
        print("Error: Student not found.")
        return False
    create_backup()
    data[student_id] = {
        "name": name,
        "department": department,
        "semester": semester,
    }
    save_students(data)
    print("Student updated successfully (Backup created).")
    return True


def delete_student(student_id):
    data = load_students()
    if student_id not in data:
        print("Error: Student not found.")
        return False
    create_backup()
    del data[student_id]
    save_students(data)
    print("Student deleted successfully (Backup created).")
    return True


if __name__ == "__main__":
    add_student("101", "Alice", "Computer Science", "3")
    add_student("102", "Bob", "Mathematics", "5")
    print("\n--- Current List ---")
    list_students()

    print("\n--- Searching 101 ---")
    search_student("101")

    print("\n--- Updating 101 ---")
    update_student("101", "Alice Smith", "Computer Science", "4")

    print("\n--- Deleting 102 ---")
    delete_student("102")

    print("\n--- Final List ---")
    list_students()
