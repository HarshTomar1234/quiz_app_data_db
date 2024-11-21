import sqlite3
import random

# Connect to the SQLite database
def connect_db():
    conn = sqlite3.connect("quiz_app.db")
    return conn

# Initialize the database (run only once to create tables)
def initialize_db():
    conn = connect_db()
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT NOT NULL,
        question TEXT NOT NULL,
        options TEXT NOT NULL,
        answer TEXT NOT NULL
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        subject TEXT NOT NULL,
        score INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )""")

    conn.commit()
    conn.close()

# Register a new user
def register_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print("Registration successful!")
    except sqlite3.IntegrityError:
        print("Username already exists!")
    finally:
        conn.close()

# Login a user
def login_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# Fetch quiz questions from the database
def get_questions(subject):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM questions WHERE subject = ?", (subject,))
    questions = cursor.fetchall()
    conn.close()
    return questions

# Save a user's score
def save_score(user_id, subject, score):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO scores (user_id, subject, score) VALUES (?, ?, ?)", (user_id, subject, score))
    conn.commit()
    conn.close()

#########################################################

# Quiz functionality
def quiz(subject, user_id):
    print(f"\nStarting {subject} quiz!")
    questions = get_questions(subject)

    if not questions:
        print(f"No questions available for {subject}.")
        return

    random.shuffle(questions)
    score = 0

    for i, q in enumerate(questions[:5], 1):
        question_id, _, question, options, answer = q
        options = options.split(",")  # Convert string to list
        print(f"\nQ{i}: {question}")
        for idx, option in enumerate(options, 1):
            print(f"{idx}. {option}")

        try:
            ans = int(input("Your answer (1/2/3/4): "))
            if options[ans - 1].strip() == answer.strip():
                print("Correct!")
                score += 1
            else:
                print(f"Wrong! The correct answer was: {answer}")
        except (ValueError, IndexError):
            print("Invalid input! Skipping this question.")

    print(f"\nYour score is {score}/5.")
    save_score(user_id, subject, score)

#########################################################

# Main application
def main():
    initialize_db()  # Run once to set up the database
    print("Welcome to the Quiz Application!")
    user = None

    while not user:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            register_user(username, password)
        elif choice == "2":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            user = login_user(username, password)
            if user:
                print("Login successful!")
            else:
                print("Invalid username or password!")
        elif choice == "3":
            print("Goodbye!")
            return
        else:
            print("Invalid choice!")

#########################################################

    while True:
        print("\nSubjects:\n1. C++\n2. Python\n3. DSA")
        choice = input("Choose a subject (1/2/3): ")

        if choice == "1":
            quiz("C++", user[0])  # Pass user ID
        elif choice == "2":
            quiz("Python", user[0])  # Pass user ID
        elif choice == "3":
            quiz("DSA", user[0])  # Pass user ID
        else:
            print("Invalid choice!")
            continue

        play_again = input("Do you want to take another quiz? (yes/no): ").lower()
        if play_again != "yes":
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
