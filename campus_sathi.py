
import mysql.connector
import hashlib
import secrets
import hmac

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "Prateek@7983",
    "database": "campus_saathi"
}

CATEGORIES = {
    "1": "Electricity",
    "2": "Water",
    "3": "Cleanliness",
    "4": "Classroom",
    "5": "Library",
    "6": "Other"
}

STATUSES = ["Pending", "In Progress", "Resolved", "Rejected"]


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def hash_password(password):
    salt = secrets.token_bytes(16)
    hashed = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), salt, 200000
    )
    return salt.hex() + "$" + hashed.hex()


def verify_password(password, saved_password):
    try:
        salt_hex, saved_hash = saved_password.split("$", 1)
        salt = bytes.fromhex(salt_hex)

        hashed = hashlib.pbkdf2_hmac(
            "sha256", password.encode(), salt, 200000
        ).hex()

        return hmac.compare_digest(hashed, saved_hash)

    except (ValueError, TypeError):
        return False



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


def submit_complaint(student):
    print("\n--- Submit Complaint ---")

    for number, category in CATEGORIES.items():
        print(number + ".", category)

    choice = input("Choose category (1-6): ").strip()

    if choice not in CATEGORIES:
        print("Invalid category.")
        return

    description = input("Describe your complaint: ").strip()

    if not description:
        print("Description cannot be empty.")
        return

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO complaints
            (student_email, category, description, status, admin_note)
            VALUES (%s, %s, %s, 'Pending', 'No note')
            """,
            (student["email"], CATEGORIES[choice], description)
        )

        conn.commit()
        complaint_id = cursor.lastrowid

        print("Complaint submitted successfully!")
        print("Complaint ID: CS" + str(complaint_id).zfill(4))
        print("Status: Pending")

    except mysql.connector.Error as error:
        print("Complaint submission error:", error)

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def view_my_complaints(student):
    print("\n--- My Complaints ---")

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, category, description, status, admin_note
            FROM complaints
            WHERE student_email = %s
            ORDER BY id DESC
            """,
            (student["email"],)
        )

        complaints = cursor.fetchall()

        if not complaints:
            print("No complaints found.")
            return

        for complaint in complaints:
            print("\n-------------------------")
            print("Complaint ID: CS" + str(complaint["id"]).zfill(4))
            print("Category:", complaint["category"])
            print("Description:", complaint["description"])
            print("Status:", complaint["status"])
            print("Admin note:", complaint["admin_note"])

    except mysql.connector.Error as error:
        print("Error:", error)

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



def admin_login():
    print("\n--- Admin Login ---")

    username = input("Enter admin username: ").strip()
    password = input("Enter admin password: ")

   
    if username == "admin" and password == "admin123":
        print("Admin login successful!")
        admin_menu()
    else:
        print("Invalid admin username or password.")


def view_all_complaints():
    print("\n--- All Complaints ---")

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT c.id, c.student_email, c.category,
                   c.description, c.status, c.admin_note,
                   s.student_id, s.name, s.course, s.building
            FROM complaints c
            LEFT JOIN students s ON s.email = c.student_email
            ORDER BY c.id DESC
            """
        )

        complaints = cursor.fetchall()

        if not complaints:
            print("No complaints found.")
            return

        for item in complaints:
            print("\n-------------------------")
            print("Complaint ID: CS" + str(item["id"]).zfill(4))
            print("Student ID:", item["student_id"])
            print("Name:", item["name"])
            print("Email:", item["student_email"])
            print("Course:", item["course"])
            print("Building:", item["building"])
            print("Category:", item["category"])
            print("Description:", item["description"])
            print("Status:", item["status"])
            print("Admin note:", item["admin_note"])

    except mysql.connector.Error as error:
        print("Error:", error)

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def update_complaint_status():
    print("\n--- Update Complaint Status ---")

    raw_id = input(
        "Enter complaint number (e.g. 1 for CS0001): "
    ).strip().upper()

    if raw_id.startswith("CS"):
        raw_id = raw_id[2:]

    if not raw_id.isdigit():
        print("Invalid complaint ID.")
        return

    complaint_id = int(raw_id)

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, status FROM complaints WHERE id = %s",
            (complaint_id,)
        )

        complaint = cursor.fetchone()
        cursor.close()
        conn.close()
        conn = None
        cursor = None

        if not complaint:
            print("Complaint not found.")
            return

        print("Current status:", complaint[1])

        for number, status in enumerate(STATUSES, 1):
            print(str(number) + ".", status)

        choice = input("Choose new status (1-4): ").strip()

        if not choice.isdigit() or not 1 <= int(choice) <= 4:
            print("Invalid status.")
            return

        status = STATUSES[int(choice) - 1]
        note = input("Admin note: ").strip() or "No note"

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE complaints
            SET status = %s, admin_note = %s
            WHERE id = %s
            """,
            (status, note, complaint_id)
        )

        conn.commit()
        print("Complaint status updated successfully.")

    except mysql.connector.Error as error:
        print("Error:", error)

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def complaint_summary():
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM complaints")
        print("Total complaints:", cursor.fetchone()[0])

        for status in STATUSES:
            cursor.execute(
                "SELECT COUNT(*) FROM complaints WHERE status = %s",
                (status,)
            )
            print(status + ":", cursor.fetchone()[0])

    except mysql.connector.Error as error:
        print("Error:", error)

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


# Admin menu
def admin_menu():
    while True:
        print("\n--- Admin Menu ---")
        print("1. View all complaints")
        print("2. Update complaint status")
        print("3. Complaint summary")
        print("4. Logout")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            view_all_complaints()
        elif choice == "2":
            update_complaint_status()
        elif choice == "3":
            complaint_summary()
        elif choice == "4":
            print("Admin logged out.")
            break
        else:
            print("Invalid choice.")


# Main menu
def main():
    while True:
        print("\n==============================")
        print("        CAMPUS SAATHI")
        print("College Complaint Management")
        print("==============================")
        print("1. Student Registration")
        print("2. Student Login")
        print("3. Admin Login")
        print("4. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            register_student()
        elif choice == "2":
            student_login()
        elif choice == "3":
            admin_login()
        elif choice == "4":
            print("Thank you for using Campus Saathi!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
