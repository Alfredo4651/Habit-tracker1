import sys
import os
import pytest

# Add the parent directory to sys.path so the analyze module can be found
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from analyze import (
    fetch_all_habits,
    fetch_habits_by_periodicity,
    fetch_all_streaks,
    fetch_streak_for_habit,
)

# NOTE: Assumes you have some sample data in your habit_tracker.db


def test_fetch_all_habits():
    """
    Test that fetch_all_habits returns a list of habit names (strings).
    """
    habits = fetch_all_habits()
    assert isinstance(habits, list)
    if habits:
        assert all(isinstance(habit, str) for habit in habits)


def test_fetch_habits_by_periodicity_daily():
    """
    Test that fetch_habits_by_periodicity correctly filters 'daily' habits.
    """
    daily_habits = fetch_habits_by_periodicity("daily")
    assert isinstance(daily_habits, list)
    if daily_habits:
        assert all(isinstance(h, str) for h in daily_habits)


def test_fetch_habits_by_periodicity_weekly():
    """
    Test that fetch_habits_by_periodicity correctly filters 'weekly' habits.
    """
    weekly_habits = fetch_habits_by_periodicity("weekly")
    assert isinstance(weekly_habits, list)
    if weekly_habits:
        assert all(isinstance(h, str) for h in weekly_habits)


def test_fetch_all_streaks():
    """
    Test that fetch_all_streaks returns a list of tuples (habit_name, streak_count).
    """
    streaks = fetch_all_streaks()
    assert isinstance(streaks, list)
    if streaks:
        assert all(isinstance(entry, tuple) and len(entry) == 2 for entry in streaks)
        assert all(isinstance(entry[0], str) and isinstance(entry[1], int) for entry in streaks)


@pytest.mark.parametrize("habit_name", ["Drink Water", "Exercise", "Read Book"])  # Replace with real test data
def test_fetch_streak_for_habit(habit_name):
    """
    Test that fetch_streak_for_habit returns an integer streak value or None for a given habit name.
    """
    streak = fetch_streak_for_habit(habit_name)
    assert streak is None or isinstance(streak, int)
