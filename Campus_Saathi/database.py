import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "Prateek@7983",
    "database": "campus_saathi"
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)
