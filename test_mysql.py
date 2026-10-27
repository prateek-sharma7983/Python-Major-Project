
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="Prateek@7983",
    database="campus_saathi"
)

if connection.is_connected():
    print("MySQL connected successfully!")

connection.close()
