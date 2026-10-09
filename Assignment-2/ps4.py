import mysql.connector

ALLOWED_COLUMNS = {
    "student.id": "s.student_id",
    "student.name": "s.name",
    "student.spi": "s.spi",
    "course.id": "c.course_id",
    "course.name": "c.course_name"
}

def build_query(columns, filters, order_column, direction, limit):
    if not columns or any(c not in ALLOWED_COLUMNS for c in columns):
        raise ValueError("Invalid column")

    if order_column not in ALLOWED_COLUMNS:
        raise ValueError("Invalid order column")

    if direction.upper() not in ("ASC", "DESC"):
        raise ValueError("Invalid sort direction")

    if not 1 <= limit <= 1000:
        raise ValueError("Invalid limit")

    selected = ", ".join(ALLOWED_COLUMNS[c] for c in columns)
    query = f"""
        SELECT {selected}
        FROM Student s
        JOIN CourseRegistration r ON s.student_id = r.student_id
        JOIN Course c ON r.course_id = c.course_id
    """

    params = []
    if filters:
        conditions = []
        for column, operator, value in filters:
            if column not in ALLOWED_COLUMNS:
                raise ValueError("Invalid filter column")
            if operator not in ("=", ">", "<", ">=", "<=", "LIKE"):
                raise ValueError("Invalid operator")
            conditions.append(f"{ALLOWED_COLUMNS[column]} {operator} %s")
            params.append(value)

        query += " WHERE " + " AND ".join(conditions)

    query += f" ORDER BY {ALLOWED_COLUMNS[order_column]} {direction.upper()}"
    query += " LIMIT %s"
    params.append(limit)

    return query, params

def main():
    try:
        columns = input("Columns: ").split(",")
        columns = [c.strip() for c in columns]

        filters = []
        text = input("Filter (column,operator,value) or blank: ").strip()

        if text:
            column, operator, value = map(str.strip, text.split(",", 2))
            filters.append((column, operator, value))

        order_column = input("Order column: ").strip()
        direction = input("Direction: ").strip()
        limit = int(input("Limit: "))

        query, params = build_query(
            columns, filters, order_column, direction, limit
        )

        print("SQL_OK")
        print(query)
        print("Parameters:", params)

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="YOUR_PASSWORD",
            database="college"
        )

        cur = conn.cursor()
        cur.execute(query, params)

        for row in cur:
            print(*row)

        cur.close()
        conn.close()

    except (ValueError, mysql.connector.Error) as e:
        print("Error:", e)

if __name__ == "__main__":
    main()