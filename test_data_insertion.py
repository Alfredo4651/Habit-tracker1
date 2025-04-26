import sqlite3
from datetime import datetime, timedelta
import os

DATABASE_URL = "habit_tracker.db"


def get_connection():
    try:
        print("Current working directory:", os.getcwd())
        conn = sqlite3.connect(DATABASE_URL)
        print(f"Connected to database: {DATABASE_URL}")
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise


def check_table_exists(table_name):
    """Check if a table exists in the database."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
            table = cursor.fetchone()
            return table is not None
    except Exception as e:
        print(f"Error checking table existence: {e}")
        raise

def insert_test_data():
    try:
        if not check_table_exists("users"):
            print("❌ Table 'users' does not exist. Exiting data insertion.")
            return

        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT habit_id, name, periodicity FROM habits WHERE user_id = 1")
            habits = cursor.fetchall()

            if not habits:
                print("ℹ️ No predefined habits found. Please make sure you run db.py first.")
                return

            # Simulated completion days for habits
            predefined_streaks = {
                1: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 16, 17, 18, 19, 22, 23, 25],  # Morning Run
                2: [1, 3, 5, 8, 10, 12, 15, 16, 17, 18, 19, 22, 26],  # Hydration
                3: [1, 2, 3, 4, 8, 9, 15, 16, 17, 18, 19, 22, 23, 24, 25, 26],  # Reading
                4: [7, 14, 28],  # Team Sync
                5: [7, 14, 21, 28],  # Grocery Shopping
            }

            for habit_id, completion_days in predefined_streaks.items():
                periodicity = next((h[2] for h in habits if h[0] == habit_id), "daily")
                streak_count = 0
                total_count = 0
                last_date = None

                for offset in sorted(completion_days):
                    current_date = (datetime.now() - timedelta(days=(max(completion_days) - offset))).date()
                    total_count += 1  # Always increase for each completed date

                    if last_date:
                        day_diff = (current_date - last_date).days
                        if (periodicity == "daily" and day_diff == 1) or \
                           (periodicity == "weekly" and 1 <= day_diff <= 7):
                            streak_count += 1
                        else:
                            streak_count = 1  # reset streak
                    else:
                        streak_count = 1

                    last_date = current_date

                # Final insert or update with full count and last completed date
                cursor.execute("SELECT count FROM streak WHERE habit_id = ? AND user_id = ?", (habit_id, 1))
                exists = cursor.fetchone()

                if exists:
                    cursor.execute("""
                        UPDATE streak
                        SET count = ?, last_completed_date = ?
                        WHERE habit_id = ? AND user_id = ?
                    """, (total_count, last_date.strftime('%Y-%m-%d %H:%M:%S'), habit_id, 1))
                else:
                    cursor.execute("""
                        INSERT INTO streak (habit_id, user_id, count, last_completed_date)
                        VALUES (?, ?, ?, ?)
                    """, (habit_id, 1, total_count, last_date.strftime('%Y-%m-%d %H:%M:%S')))

                # Update habit's last_completed_at
                cursor.execute("""
                    UPDATE habits
                    SET last_completed_at = ?
                    WHERE habit_id = ?
                """, (last_date.strftime('%Y-%m-%d %H:%M:%S'), habit_id))

            conn.commit()
            print("✅ Test data inserted with accurate streak and count values.")

    except Exception as e:
        print(f"❌ Error inserting test data: {e}")

if __name__ == "__main__":
    insert_test_data()
