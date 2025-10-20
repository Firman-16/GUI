import mysql.connector

def connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        database="perpustakaan_db"
    )
