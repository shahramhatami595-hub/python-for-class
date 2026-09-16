import os

filename = "students.txt"

initial_records = [
    "101,Alice,Computer Science\n",
    "102,Bob,Mathematics\n",
    "103,Charlie,Physics\n",
    "104,David,Chemistry\n",
    "105,Eve,Biology\n"
]

with open(filename, "w") as file:
    file.writelines(initial_records)

try:
    with open(filename, "r") as file:
        print("--- All Records ---")
        print(file.read().strip())
except FileNotFoundError:
    print(f"Error: {filename} does not exist.")

search_id = "103"
try:
    with open(filename, "r") as file:
        found = False
        for line in file:
            if line.startswith(search_id + ","):
                print(f"--- Found Student ({search_id}) ---")
                print(line.strip())
                found = True
                break
        if not found:
            print("Student not found.")
except FileNotFoundError:
    print(f"Error: {filename} does not exist.")

new_student = "106,Frank,History\n"
try:
    with open(filename, "a") as file:
        file.write(new_student)
except FileNotFoundError:
    print(f"Error: {filename} does not exist.")

try:
    with open(filename, "r") as file:
        count = sum(1 for line in file)
        print(f"--- Total Records: {count} ---")
except FileNotFoundError:
    print(f"Error: {filename} does not exist.")