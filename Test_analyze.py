import pytest

import sqlite3

from datetime import datetime

from analyze import fetch_all_habits, fetch_habits_by_periodicity, fetch_all_streaks, fetch_streak_for_habit





# -------------------------

# Test Database Setup (Use an in-memory database to avoid locking)

# -------------------------



@pytest.fixture

def mock_db():

    """Fixture to connect to a new in-memory SQLite database for testing."""

    # Using an in-memory database to avoid file locking issues

    conn = sqlite3.connect(":memory:")

    cursor = conn.cursor()



    # Create the schema

    cursor.execute("""

    CREATE TABLE habits (

        habit_id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT UNIQUE,

        periodicity TEXT NOT NULL,

        created_at TEXT NOT NULL

    )""")



    cursor.execute("""

    CREATE TABLE streak (

        streak_id INTEGER PRIMARY KEY AUTOINCREMENT,

        habit_id INTEGER,

        count INTEGER NOT NULL,

        FOREIGN KEY (habit_id) REFERENCES habits(habit_id)

    )""")



    # Insert test data with a valid created_at value

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")



    # Ensure no unique constraint violation by deleting the habit if it already exists

    cursor.execute("DELETE FROM habits WHERE name = 'Exercise'")

    cursor.execute("DELETE FROM habits WHERE name = 'Reading'")

    cursor.execute("DELETE FROM habits WHERE name = 'Meditation'")



    cursor.execute("INSERT INTO habits (name, periodicity, created_at) VALUES ('Exercise', 'daily', ?)",

                   (current_time,))

    cursor.execute("INSERT INTO habits (name, periodicity, created_at) VALUES ('Reading', 'weekly', ?)",

                   (current_time,))

    cursor.execute("INSERT INTO habits (name, periodicity, created_at) VALUES ('Meditation', 'daily', ?)",

                   (current_time,))



    # Assuming habit_id = 1, 2, 3 respectively for simplicity

    cursor.execute("INSERT INTO streak (habit_id, count) VALUES (1, 5)")

    cursor.execute("INSERT INTO streak (habit_id, count) VALUES (2, 3)")



    conn.commit()

    yield cursor  # Provide the test DB connection to the test functions



    # Cleanup after test

    conn.close()





# -------------------------

# Test Functions

# -------------------------



def test_fetch_all_habits(mock_db):

    """Test the fetch_all_habits function."""

    habits = fetch_all_habits(mock_db)

    assert "Exercise" in habits

    assert "Reading" in habits

    assert "Meditation" in habits





def test_fetch_habits_by_periodicity(mock_db):

    """Test the fetch_habits_by_periodicity function."""

    daily_habits = fetch_habits_by_periodicity(mock_db, "daily")

    weekly_habits = fetch_habits_by_periodicity(mock_db, "weekly")



    assert "Exercise" in daily_habits

    assert "Meditation" in daily_habits

    assert "Reading" in weekly_habits





def test_fetch_all_streaks(mock_db):

    """Test the fetch_all_streaks function."""

    streaks = fetch_all_streaks(mock_db)

    assert ("Exercise", 5) in streaks

    assert ("Reading", 3) in streaks





def test_fetch_streak_for_habit(mock_db):

    """Test the fetch_streak_for_habit function."""

    streak_exercise = fetch_streak_for_habit(mock_db, "Exercise")

    streak_reading = fetch_streak_for_habit(mock_db, "Reading")

    streak_meditation = fetch_streak_for_habit(mock_db, "Meditation")



    assert streak_exercise == 5

    assert streak_reading == 3

    assert streak_meditation is None  # No streak data for Meditation





# -------------------------

# Run the tests

# -------------------------



if __name__ == "__main__":

    pytest.main()