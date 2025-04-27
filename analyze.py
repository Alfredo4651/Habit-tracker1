from typing import Any, List, Tuple

from db import get_connection
import questionary
from functools import reduce


# ---------------------------
# Helper functions (functional style)
# ---------------------------

def fetch_all_habits(cursor) -> List[str]:
    """
    Retrieve the names of all habits from the database using the provided cursor.
    Returns a list of habit names.
    """
    cursor.execute("SELECT name FROM habits")
    return list(map(lambda row: row[0], cursor.fetchall()))


def fetch_habits_by_periodicity(cursor, periodicity: str) -> List[str]:
    """
    Retrieve the names of habits that match the given periodicity (daily/weekly)
    using the provided cursor.

    Args:
        cursor: The database cursor object.
        periodicity (str): The periodicity to filter by ("daily" or "weekly").

    Returns:
        list: A list of habit names matching the given periodicity.
    """
    cursor.execute("SELECT name FROM habits WHERE periodicity = ?", (periodicity,))
    return list(map(lambda row: row[0], cursor.fetchall()))


def fetch_all_streaks(cursor) -> List[Tuple[str, int]]:
    """
    Retrieve all habit names along with their associated streak counts
    using the provided cursor.

    Returns:
        list of tuples: Each tuple contains a habit name and its streak count.
    """
    cursor.execute("""
        SELECT h.name, s.count
        FROM habits h
        JOIN streak s ON h.habit_id = s.habit_id
    """)
    return cursor.fetchall()


def fetch_streak_for_habit(cursor, habit_name: str) -> Any | None:
    """
    Retrieve the streak count for a specific habit by name
    using the provided cursor.

    Args:
        cursor: The database cursor object.
        habit_name (str): The name of the habit.

    Returns:
        int or None: The streak count if found, otherwise None.
    """
    cursor.execute("""
        SELECT s.count
        FROM habits h
        JOIN streak s ON h.habit_id = s.habit_id
        WHERE h.name = ?
    """, (habit_name,))
    result = cursor.fetchone()
    return result[0] if result else None


# ---------------------------
# Analytics Interface
# ---------------------------

def run_analytics():
    """
    Display the interactive analytics menu and handle user-selected options
    for analyzing tracked habits and their streaks.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        while True:
            choice = questionary.select(
                "📊 Analytics Menu - Choose an analysis option:",
                choices=[
                    "List all currently tracked habits",
                    "List habits by periodicity",
                    "Longest streak across all habits",
                    "Longest streak for a specific habit",
                    "Back to Main Menu"
                ]
            ).ask()

            # Option 1: Display all tracked habits
            if choice == "List all currently tracked habits":
                habits = fetch_all_habits(cursor)
                if habits:
                    questionary.print("📋 Tracked Habits:")
                    list(map(lambda h: questionary.print(f"- {h}"), habits))
                else:
                    questionary.print("⚠️ No habits found.")

            # Option 2: Display habits by user-specified periodicity
            elif choice == "List habits by periodicity":
                period = questionary.select(
                    "Select periodicity:",
                    choices=["daily", "weekly"]
                ).ask()
                habits = fetch_habits_by_periodicity(cursor, period)
                if habits:
                    questionary.print(f"📅 {period.capitalize()} Habits:")
                    list(map(lambda h: questionary.print(f"- {h}"), habits))
                else:
                    questionary.print(f"⚠️ No {period} habits found.")

            # Option 3: Find and display the longest streak among all habits
            elif choice == "Longest streak across all habits":
                streaks = fetch_all_streaks(cursor)
                if streaks:
                    longest = reduce(lambda a, b: a if a[1] > b[1] else b, streaks)
                    questionary.print(f"🏆 Longest Streak: {longest[0]} with {longest[1]} completions")
                else:
                    questionary.print("⚠️ No streak data available.")

            # Option 4: Retrieve and display the streak for a specific habit
            elif choice == "Longest streak for a specific habit":
                habit_name = questionary.text("Enter the habit name:").ask()
                streak = fetch_streak_for_habit(cursor, habit_name)
                if streak:
                    questionary.print(f"🔥 '{habit_name}' has a streak of {streak} completions.")
                else:
                    questionary.print(f"⚠️ No streak found for '{habit_name}'.")

            # Option 5: Exit the analytics menu
            elif choice == "Back to Main Menu":
                break
