from student import register_student, student_login
from admin import admin_login

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
