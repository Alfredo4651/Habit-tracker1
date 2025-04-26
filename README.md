# Habit Tracker

Habit Tracker is a Python-based command-line interface (CLI) application that allows users to create, edit, track, and analyze their habits. It provides a user-friendly interface for managing periodic tasks and helps users maintain streaks and analyze their habits' progress.

## Table of Contents
- [Features](#features)
  - [User Management](#user-management)
  - [Habit Management](#habit-management)
  - [Analytics](#analytics)
  - [Interface](#interface)
- [Technical Requirements](#technical-requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Main Commands](#main-commands)
  - [Analytics Commands](#analytics-commands)
  - [Test Data Generation](#test-data-generation)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)

## Features

### User Management
- Secure user authentication system.
- Individual user profiles.
- Predefined habit templates for new users.

### Habit Management
- Create, edit, and delete habits.
- Mark habits as complete.
- Daily and weekly habit tracking.
- Customizable habit descriptions.
- Streak tracking system.

### Analytics
- View currently tracked habits.
- Filter habits by periodicity (daily, weekly).
- Track longest running streaks.
- Analyze habit completion patterns.

### Interface
- User-friendly CLI.
- Interactive menu system.
- Clear command structure.
- Real-time feedback.

## Technical Requirements

- Python 3.7+
- SQLite3
- Virtual Environment

## Installation

To install and set up the Habit Tracker project, follow these steps:

1. **Clone the repository**:

    ```bash
    git clone https://github.com/Alfredo4651/Habit-tracker1.git
    ```

2. **Navigate to the project directory**:

    ```bash
    cd habit-tracker
    ```

3. **Set up the virtual environment**:

    For **Windows**:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

    For **Mac/Linux**:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

4. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

5. **Set up the database**:

    Before running the main application, you **must** create the database tables:

    ```bash
    python db.py
    ```

6. **Insert test data (optional but recommended)**:

    After setting up the database, insert predefined sample data for testing:

    ```bash
    python test_data_insertion.py
    ```

7. **Run the main application**:

    ```bash
    python main.py
    ```

---

## Usage

Once successfully registered and logged in, use the commands to navigate the app.

### Main Commands
- **1** - Register
- **2** - View profile
- **3** - Add habit
- **4** - View Habits
- **5** - Log Habit Completion
- **6** - Delete Habit
- **7** - Delete Account
- **8** - Analytics
- **Exit** - Exit the application

### Analytics Commands
- **1** - List all currently tracked habits
- **2** - List habits by periodicity
- **3** - Longest streak across all habits
- **4** - Longest streak for a specific habit
- **Back** - Back to Main Menu

### Test Data Generation
Sample data can be added via the `test_data_insertion.py` script to simulate habits for different users.

---

## Testing

The project uses `pytest` for testing key functionality.

**Note**: Test should be run after running **python db.py** and python **test_data_insertion** in the terminal.

To run all tests:

```bash
pytest
```

The following tests are included:

```python
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
```

### Test Coverage

- ✅ test_fetch_all_habits.
- ✅ test_fetch_habits_by_periodicity_daily.
- ✅ test_fetch_habits_by_periodicity_weekly.
- ✅ test_fetch_all_streaks.
- ✅ test_fetch_streak_for_habit[Drink Water]
- ✅ test_fetch_streak_for_habit[Exercise]
- ✅ test_fetch_streak_for_habit[Read Book]
---

## Project Structure

```bash
habit-tracker/
├── analyze.py
├── .gitignore
├── db.py
├── habit_tracker.db
├── main.py
├── test_data_insertion.py
├── test_concept.py
├── README.md
└── requirements.txt
```

---

## Dependencies

The following Python packages are used in this project:

```bash
pytest
Questionary
sqlite3 (standard library)
os (standard library)
datetime (standard library)
```

Install all dependencies with:

```bash
pip install -r requirements.txt
```

---

