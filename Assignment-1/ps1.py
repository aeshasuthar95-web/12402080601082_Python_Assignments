
# Assignment 1 - Q1
# Campus Merit Analyzer using Compound Data Structures


def main():
    # Read n = number of students,
    # k = number of top students required,
    # m = number of subjects
    n, k, m = map(int, input().split())

    # Basic input validation
    if not (1 <= n <= 100000):
        raise ValueError("Number of students must be between 1 and 100000.")

    if not (1 <= k <= 50):
        raise ValueError("K must be between 1 and 50.")

    if not (1 <= m <= 12):
        raise ValueError("Number of subjects must be between 1 and 12.")

    # Dictionary:
    # semester -> list of student records
    semester_students = {}

    # Dictionary:
    # subject code -> (highest mark, list of enrollments)
    subject_toppers = {}

    # Initialize subject topper information
    for i in range(1, m + 1):
        subject_toppers[f"S{i}"] = (-1, [])

    # ---------------------------------------------------------
    # Read student records
    # ---------------------------------------------------------
    for _ in range(n):
        data = input().split()

        # First four values are:
        # enrollment, name, semester, CPI
        enrollment = data[0]
        name = data[1]
        semester = int(data[2])
        cpi = float(data[3])

        # Remaining m values are subject marks
        marks = list(map(int, data[4:]))

        # Validate number of marks
        if len(marks) != m:
            raise ValueError(
                f"{enrollment} must have exactly {m} subject marks."
            )

        # Validate marks
        if any(mark < 0 or mark > 100 for mark in marks):
            raise ValueError("Marks must be between 0 and 100.")

        # Validate semester and CPI
        if not (1 <= semester <= 8):
            raise ValueError("Semester must be between 1 and 8.")

        if not (0.0 <= cpi <= 10.0):
            raise ValueError("CPI must be between 0.0 and 10.0.")

        # Calculate average marks
        average_marks = sum(marks) / m

        # Store student information as a tuple.
        # Tuple contains:
        # enrollment, name, CPI, average marks, marks
        student = (
            enrollment,
            name,
            cpi,
            average_marks,
            marks
        )

        # Add student to the appropriate semester
        if semester not in semester_students:
            semester_students[semester] = []

        semester_students[semester].append(student)

        # -----------------------------------------------------
        # Update subject-wise topper information
        # -----------------------------------------------------
        for i, mark in enumerate(marks, start=1):
            subject = f"S{i}"

            highest_mark, toppers = subject_toppers[subject]

            if mark > highest_mark:
                # New highest mark found
                subject_toppers[subject] = (mark, [enrollment])

            elif mark == highest_mark:
                # Another student has the same highest mark
                toppers.append(enrollment)

    # ---------------------------------------------------------
    # Print semester-wise top K students
    # ---------------------------------------------------------
    for semester in sorted(semester_students):

        students = semester_students[semester]

        # Ranking priority:
        # 1. Higher CPI
        # 2. Higher average marks
        # 3. Lexicographically smaller enrollment
        #
        # Python's sort is ascending, so:
        # - CPI uses negative value
        # - Average marks uses negative value
        students.sort(
            key=lambda student: (
                -student[2],       # Higher CPI first
                -student[3],       # Higher average marks first
                student[0]         # Smaller enrollment first
            )
        )

        # Take only top K students
        top_students = students[:k]

        enrollments = [student[0] for student in top_students]

        print(f"Semester {semester}:", *enrollments)

    # ---------------------------------------------------------
    # Print subject-wise toppers
    # ---------------------------------------------------------
    for i in range(1, m + 1):
        subject = f"S{i}"

        highest_mark, toppers = subject_toppers[subject]

        # Sort enrollment numbers lexicographically
        toppers.sort()

        print(f"{subject}:", *toppers)


# Program execution
if __name__ == "__main__":
    main()