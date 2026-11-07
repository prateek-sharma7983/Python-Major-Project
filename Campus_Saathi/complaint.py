import mysql.connector
from database import get_connection

CATEGORIES = {
    "1": "Electricity",
    "2": "Water",
    "3": "Cleanliness",
    "4": "Classroom",
    "5": "Library",
    "6": "Other"
}


STATUSES = ["Pending", "In Progress", "Resolved", "Rejected"]


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
