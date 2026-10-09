
import pyodbc

from config import SERVER, DATABASE, DRIVER


def create_connection():
    """SQL Server verilənlər bazasına bağlantı yaradır."""

    connection_string = (
        f"DRIVER={DRIVER};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )

    return pyodbc.connect(connection_string)


def add_student(student_name, score):
    """Yeni tələbəni verilənlər bazasına əlavə edir."""

    connection = create_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO Students (StudentName, Score)
            VALUES (?, ?)
            """,
            (student_name, score)
        )

        connection.commit()

    finally:
        connection.close()


def get_students():
    """Bütün tələbələri verilənlər bazasından qaytarır."""

    connection = create_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT StudentID, StudentName, Score
            FROM Students
            ORDER BY StudentID
            """
        )

        students = []

        for row in cursor.fetchall():
            students.append({
                "StudentID": row[0],
                "Name": row[1],
                "Score": row[2]
            })

        return students

    finally:
        connection.close()


def get_student(student_name):
    """Adına görə tələbələri axtarır."""

    connection = create_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT StudentID, StudentName, Score
            FROM Students
            WHERE StudentName LIKE ?
            ORDER BY StudentName
            """,
            (f"%{student_name}%",)
        )

        students = []

        for row in cursor.fetchall():
            students.append({
                "StudentID": row[0],
                "Name": row[1],
                "Score": row[2]
            })

        return students

    finally:
        connection.close()
