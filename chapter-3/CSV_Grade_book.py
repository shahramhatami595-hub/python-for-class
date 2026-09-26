import csv

filename = "gradebook.csv"
output_filename = "results.csv"

data = [
    {"student_id": "1", "name": "John Doe", "midterm": "85", "final": "90"},
    {"student_id": "2", "name": "Jane Smith-Rowe", "midterm": "45", "final": "50"},
    {"student_id": "3", "name": "Bob O'Brian", "midterm": "70", "final": "75"},
    {"student_id": "4", "name": "Alice, Jr.", "midterm": "95", "final": "92"},
    {"student_id": "5", "name": "Charlie", "midterm": "60", "final": "55"}
]

with open(filename, "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["student_id", "name", "midterm", "final"])
    writer.writeheader()
    writer.writerows(data)

results = []
threshold = 70

with open(filename, "r", newline="") as file:
    reader = csv.DictReader(file)
    for row in reader:
        midterm = float(row["midterm"])
        final = float(row["final"])
        average = (midterm + final) / 2
        
        row["average"] = average
        results.append(row)
        
        if average >= threshold:
            print(f"Passed: {row['name']} (Average: {average})")

with open(output_filename, "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["student_id", "name", "midterm", "final", "average"])
    writer.writeheader()
    writer.writerows(results)
