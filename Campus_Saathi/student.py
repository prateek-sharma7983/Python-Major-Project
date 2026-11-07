import mysql.connector
from database import get_connection
from security import hash_password, verify_password
from complaint import submit_complaint, view_my_complaints

def register_student():
    print("\n--- Student Registration ---")

    student_id = input("Enter Student ID: ").strip()
    name = input("Enter your name: ").strip()
    email = input("Enter your email: ").strip().lower()
    course = input("Enter your course: ").strip()
    building = input("Enter your building/block: ").strip()
    password = input("Create password (minimum 8 characters): ")

    if not all([student_id, name, email, course, building, password]):
        print("All fields are required.")
        return

    if "@" not in email or "." not in email.split("@")[-1]:
        print("Please enter a valid email.")
        return

    if len(password) < 8:
        print("Password must be at least 8 characters.")
        return

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id FROM students
            WHERE email = %s OR student_id = %s
            """,
            (email, student_id)
        )

        if cursor.fetchone():
            print("Email or Student ID already registered.")
            return

        cursor.execute(
            """
            INSERT INTO students
            (student_id, name, email, course, building, password)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                student_id,
                name,
                email,
                course,
                building,
                hash_password(password)
            )
        )

        conn.commit()
        print("Registration successful!")

    except mysql.connector.Error as error:
        print("Registration error:", error)

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def student_login():
    print("\n--- Student Login ---")

    email = input("Enter your email: ").strip().lower()
    password = input("Enter your password: ")

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, student_id, name, email, course,
                   building, password
            FROM students
            WHERE email = %s
            """,
            (email,)
        )

        student = cursor.fetchone()

        if student and verify_password(password, student["password"]):
            print("\nLogin successful!")
            print("Welcome,", student["name"])
            student_menu(student)
        else:
            print("Invalid email or password.")

    except mysql.connector.Error as error:
        print("Login error:", error)

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def student_menu(student):
    while True:
        print("\n--- Student Menu ---")
        print("Student ID:", student["student_id"])
        print("Course:", student["course"])
        print("Building:", student["building"])
        print("1. Submit complaint")
        print("2. View my complaints")
        print("3. Logout")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            submit_complaint(student)
        elif choice == "2":
            view_my_complaints(student)
        elif choice == "3":
            print("Logged out.")
            break
        else:
            print("Invalid choice.")
