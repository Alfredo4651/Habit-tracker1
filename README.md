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
- **Secure user authentication system.**
- **Individual user profiles.**
- **Predefined habit templates for new users.**

### Habit Management
- **Create, edit, and delete habits.**
- **Mark habits as complete.**
- **Daily and weekly habit tracking.**
- **Customizable habit descriptions.**
- **Streak tracking system.**

### Analytics
- **View currently tracked habits.**
- **Filter habits by periodicity (daily, weekly).**
- **Track longest running streaks.**
- **Analyze habit completion patterns.**

### Interface
- **User-friendly CLI.**
- **Interactive menu system.**
- **Clear command structure.**
- **Real-time feedback.**

## Technical Requirements

- **Python 3.7+**
- **SQLite3**
- **pytest**
- **Questionary**
- **Virtual Environment**

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

The project uses `pytest` for testing key functionality, run  **test_concept.py** and  **test_analyze**.

**Note**: Test should be run after running **python db.py** and **python test_data_insertion.py** in the terminal.

To run all tests:

```bash
pytest


habit-tracker/
├── analyze.py
├── .gitignore
├── db.py
├── habit_tracker.db
├── main.py
├── test_data_insertion.py
├── test_concept.py
├── test_analyze.py
├── README.md
└── requirements.txt


pytest
Questionary
sqlite3 (standard library)
os (standard library)
datetime (standard library)


pip install -r requirements.txt


