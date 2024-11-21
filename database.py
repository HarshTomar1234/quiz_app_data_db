import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("quiz_app.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT NOT NULL,
    question TEXT NOT NULL,
    options TEXT NOT NULL,
    answer TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    subject TEXT NOT NULL,
    score INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
""")

print("Database and tables created successfully!")

# Commit changes and close connection
conn.commit()
conn.close()
