import sqlite3

DB_NAME = "alumni.db"

def create_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alumni (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            graduation_year INTEGER,
            course TEXT,
            profession TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_alumni(name, email, year, course, profession):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO alumni (name, email, graduation_year, course, profession)
        VALUES (?, ?, ?, ?, ?)
    """, (name, email, year, course, profession))
    conn.commit()
    conn.close()

def view_alumni():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alumni")
    data = cursor.fetchall()
    conn.close()
    return data
