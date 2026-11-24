
# 🎓 CampusCare

### A Python CLI-Based Application with MySQL Database Integration

A command-line application designed to simplify student complaint management in educational institutions. The system allows students to register, log in, submit complaints, and track their complaint status, while administrators can manage complaints and update their resolution status.

---

## 📌 Project Overview

The Student Complaint Management System is developed using Python and MySQL.

It provides a structured platform where students can submit complaints related to college facilities, laboratories, classrooms, and other academic services.

The administrator can view registered students, review submitted complaints, and update their status as Pending, In Progress, or Solved.

The application automatically creates the required database and tables when it runs, reducing the need for manual database setup.

---

## ✨ Features

### 👨‍🎓 Student Module

- Student Registration
- Unique Student ID
- Secure Password Hashing
- Student Login Authentication
- Course and Course Year Management
- Submit New Complaints
- View Personal Complaints
- Track Complaint Status
- Secure Logout

### 👨‍💼 Admin Module

- First-Time Admin Account Setup
- Admin Login Authentication
- View All Registered Students
- View All Submitted Complaints
- View Pending Complaints
- View In Progress Complaints
- View Solved Complaints
- Update Complaint Status
- Secure Logout

### 🗄️ Database Features

- Automatic Database Creation
- Automatic Table Creation
- MySQL Database Integration
- Unique Student ID Validation
- Primary and Foreign Key Constraints
- Automatic Complaint ID Generation
- Complaint Creation and Update Timestamps
- Persistent Data Storage

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application Logic |
| MySQL | Database Management |
| MySQL Connector/Python | Python–MySQL Connectivity |
| MySQL Workbench | Database Inspection |
| VS Code | Development Environment |
| Git & GitHub | Version Control |

---

## 📂 Project Structure

```text
campuscare/
│
├── main.py
├── database.py
├── security.py
├── student.py
├── admin.py
├── complaint.py
│
├── requirements.txt
└── README.md
```

---

## 🚀 How It Works

1. The application starts through `main.py`.
2. The database module establishes a connection with MySQL.
3. Required database and tables are created automatically.
4. Students can register and log in to their accounts.
5. Students can submit complaints and track their status.
6. Administrators can view and manage all complaints.
7. Complaint statuses can be updated to Pending, In Progress, or Solved.

---

## 🔐 Security

- Passwords are stored using secure hashing.
- Student and administrator login authentication.
- Unique Student ID validation.
- Database constraints for maintaining data integrity.

---

## 🎯 Project Objective

The main objective of CampusCare is to digitize and simplify the traditional complaint management process in educational institutions.

It provides a centralized platform for students to submit complaints and allows administrators to manage and resolve them efficiently.

---

## 👨‍💻 Author

**Prateek Sharma**

GitHub: [prateek-sharma7983](https://github.com/prateek-sharma7983)

---

⭐ If you find this project useful, don't forget to give it a star!
