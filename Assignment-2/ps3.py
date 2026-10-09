import csv

def main():
    student_file = input("Student CSV: ").strip()
    registration_file = input("Registration CSV: ").strip()
    course_id = input("Course ID: ").strip()

    try:
        threshold = float(input("SPI threshold: "))
        if not 0 <= threshold <= 10:
            print("Invalid SPI threshold.")
            return

        students = {}

        with open(student_file, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                students[row["student_id"]] = {
                    "name": row["name"],
                    "spi": float(row["spi"])
                }

        result = []

        with open(registration_file, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                sid = row["student_id"]

                if row["course_id"] == course_id and sid in students:
                    if students[sid]["spi"] > threshold:
                        result.append((
                            sid,
                            students[sid]["name"],
                            students[sid]["spi"],
                            row["course_id"]
                        ))

        result.sort(key=lambda x: (-x[2], x[0]))

        for row in result:
            print(*row)

    except FileNotFoundError:
        print("File not found.")
    except (ValueError, KeyError):
        print("Invalid CSV data.")

if __name__ == "__main__":
    main()