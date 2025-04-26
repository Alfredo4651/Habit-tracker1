import sqlite3
from datetime import datetime
import os

# Path to the SQLite database file
DATABASE_URL = "habit_tracker.db"


def get_connection():
    """
    Establishes and returns a connection to the SQLite database.
    Includes debugging statements to print the current working directory
    and confirm successful connection.

    Returns:
        sqlite3.Connection: A connection object to the database.
    """
    try:
        # Debugging: Display the current working directory
        print("Current working directory:", os.getcwd())

        # Attempt to connect to the database
        conn = sqlite3.connect(DATABASE_URL)
        print(f"Connected to database: {DATABASE_URL}")
        return conn
    except Exception as e:
        # Handle connection errors
        print(f"Error connecting to database: {e}")
        raise


def create_tables():
    """
    Creates the necessary tables in the database if they do not already exist:
    - users: stores registered user credentials
    - habits: stores user habits with periodicity and timestamps
    - streak: tracks completion streaks for each habit
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            # Create 'users' table to store usernames and passwords
            cursor.execute(''' 
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                )
            ''')

            # Create 'habits' table to store habits and their metadata
            cursor.execute(''' 
                CREATE TABLE IF NOT EXISTS habits (
                    habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    description TEXT,
                    periodicity TEXT CHECK(periodicity IN ('daily', 'weekly')) NOT NULL,
                    created_at TEXT NOT NULL,
                    last_completed_at TEXT,
                    user_id INTEGER,
                    is_active TEXT DEFAULT 'Yes',
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                )
            ''')

            # Create 'streak' table to track how many times a habit has been completed
            cursor.execute(''' 
                CREATE TABLE IF NOT EXISTS streak (
                    streak_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    habit_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    count INTEGER DEFAULT 0,
                    last_completed_date TEXT,
                    FOREIGN KEY (habit_id) REFERENCES habits(habit_id) ON DELETE CASCADE,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                )
            ''')

            # Commit the changes to the database
            conn.commit()
            print("Tables created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")
        raise


def insert_user(username, password):
    """
    Inserts a new user into the database if the username doesn't already exist.

    Args:
        username (str): The username of the new user.
        password (str): The password of the new user.

    Returns:
        int or None: The user ID of the newly inserted (or existing) user,
                     or None if insertion failed.
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            # Check if the user already exists
            cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            if row:
                print(f"ℹ️ User '{username}' already exists.")
                return row[0]

            # Insert new user credentials
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            print(f"✅ User '{username}' inserted successfully!")
            return cursor.lastrowid
    except Exception as e:
        print(f"❌ Error inserting user: {e}")
        return None


def initialize_predefined_habits(user_id):
    """
    Inserts a predefined list of daily and weekly habits for the given user ID.

    Args:
        user_id (int): The ID of the user to assign the predefined habits to.
    """
    # Predefined habit templates with name, description, and frequency
    predefined_habits = [
        ("Morning Run", "Jog for 20 minutes in the morning", "daily"),
        ("Hydration", "Drink 8 glasses of water", "daily"),
        ("Reading", "Read at least 10 pages of a book", "daily"),
        ("Team Sync", "Attend weekly team meeting", "weekly"),
        ("Grocery Shopping", "Do weekly grocery shopping", "weekly")
    ]

    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            # Loop through and insert each predefined habit
            for name, description, periodicity in predefined_habits:
                cursor.execute(''' 
                    INSERT INTO habits (name, description, periodicity, created_at, last_completed_at, user_id, is_active) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    name, description, periodicity, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), None, user_id, 'Yes'))

            conn.commit()
            print("✅ Predefined habits initialized successfully.")
    except Exception as e:
        print(f"❌ Error initializing predefined habits: {e}")
        raise


def populate():
    """
    Populates the database with a test user and initializes predefined habits.
    Acts as a test seed for development or testing environments.
    """
    # Insert a test user into the users table
    user_id = insert_user("test_user", "password123")
    if user_id:
        # Add predefined habits if the user was successfully inserted
        initialize_predefined_habits(user_id)
    else:
        print("❌ No test data populated. User insertion failed.")


if __name__ == "__main__":
    # Debugging: Check if database file exists before and after operations
    print("Before running db.py:", os.path.exists(DATABASE_URL))

    # Create necessary tables and populate initial test data
    create_tables()
    populate()

    print("After running db.py:", os.path.exists(DATABASE_URL))
