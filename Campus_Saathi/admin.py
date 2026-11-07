import mysql.connector
from database import get_connection
from complaint import STATUSES

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
