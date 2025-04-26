from datetime import datetime  # Import datetime module for working with dates and times
import questionary  # Import questionary for user input and interaction
from db import get_connection  # Import the function to get a database connection from the db module
from analyze import run_analytics  # Import the analytics function for viewing analytics


# ---------------------------
# Register a new user
# ---------------------------
def register():
    # Prompt the user for a username and password using questionary
    username = questionary.text("Choose your desired username:").ask()
    password = questionary.password("Enter your password:").ask()

    # Insert the username and password into the database
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",  # SQL query to insert the user
            (username, password)
        )
        conn.commit()  # Commit the transaction to save the user in the database

    # Print confirmation message
    questionary.print(f"✅ User '{username}' registered successfully!")


# ---------------------------
# Add a new habit
# ---------------------------
def add_habit():
    # Prompt for username and user ID
    username = questionary.text("Enter your username:").ask()
    user_id_input = questionary.text("Enter your user ID:").ask()

    # Attempt to convert user_id_input to an integer, if it fails, show an error
    try:
        user_id = int(user_id_input)
    except ValueError:
        questionary.print("❌ Invalid user ID. Must be a number.")
        return

    # Open a connection to the database
    with get_connection() as conn:
        cursor = conn.cursor()

        # Check if the username exists in the users table
        cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        # If no user is found or user ID does not match, print error
        if not user or user[0] != user_id:
            questionary.print("❌ Username and User ID do not match.")
            return

        # Prompt for the habit name, description, and periodicity (daily or weekly)
        name = questionary.text("Enter the habit name:").ask()
        description = questionary.text("Enter a description (optional):").ask()
        periodicity = questionary.select("Choose the frequency of the habit:", choices=["daily", "weekly"]).ask()
        created_at = datetime.now()  # Get the current time for habit creation

        # Check if the habit already exists for the user
        cursor.execute("SELECT * FROM habits WHERE user_id = ? AND name = ?", (user_id, name))
        existing = cursor.fetchone()

        # If the habit exists, print an error
        if existing:
            questionary.print(f"❌ Habit '{name}' already exists for this user.")
        else:
            # Insert the new habit into the database
            cursor.execute("""
                INSERT INTO habits (name, description, periodicity, created_at, user_id, is_active)
                VALUES (?, ?, ?, ?, ?, 'Yes')
            """, (name, description, periodicity, created_at, user_id))
            conn.commit()  # Commit the transaction
            questionary.print(f"✅ Habit '{name}' added successfully!")


# ---------------------------
# View the list of a user's habits
# ---------------------------
def view_habit():
    # Prompt for username and password to authenticate
    username = questionary.text("Enter your username:").ask()
    password = questionary.password("Enter your password:").ask()

    # Open a connection to the database and check user credentials
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()

        # If no user is found, print error
        if not user:
            questionary.print("❌ Invalid username or password.")
            return

        user_id = user[0]

        # Query the user's habits
        cursor.execute("""
            SELECT habit_id, name, description, periodicity, is_active, last_completed_at
            FROM habits
            WHERE user_id = ?
        """, (user_id,))
        habits = cursor.fetchall()

        # If habits are found, print them
        if habits:
            questionary.print(f"📋 Habits for '{username}':")
            for habit in habits:
                questionary.print(
                    f"- ID {habit[0]}: {habit[1]} | {habit[2]} | Frequency: {habit[3]} | Active: {habit[4]} | Last Completed: {habit[5]}"
                )
        else:
            # If no habits are found, print a message
            questionary.print("⚠️ You have no habits yet.")


# ---------------------------
# Log a habit completion
# ---------------------------
def log_completion():
    # Prompt for username, user ID, and habit ID
    username = questionary.text("Enter your username:").ask()
    user_id_input = questionary.text("Enter your user ID:").ask()
    habit_id_input = questionary.text("Enter the Habit ID you completed:").ask()
    completed_at = datetime.now()  # Time of habit completion
    today = completed_at.date()  # Today's date

    # Attempt to convert user_id and habit_id to integers
    try:
        user_id = int(user_id_input)
        habit_id = int(habit_id_input)
    except ValueError:
        questionary.print("❌ Invalid user ID or Habit ID. Must be numbers.")
        return

    # Open a connection to the database
    with get_connection() as conn:
        cursor = conn.cursor()

        # Check if the username exists
        cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        if not user or user[0] != user_id:
            questionary.print("❌ Username and User ID do not match.")
            return

        # Check if the habit exists for the user
        cursor.execute("SELECT periodicity FROM habits WHERE habit_id = ? AND user_id = ?", (habit_id, user_id))
        habit = cursor.fetchone()
        if not habit:
            questionary.print("❌ Habit not found or doesn't belong to the user.")
            return

        # Check and update the streak for the habit
        cursor.execute("SELECT count FROM streak WHERE habit_id = ? AND user_id = ?", (habit_id, user_id))
        streak = cursor.fetchone()

        if streak:
            count = streak[0] + 1
            cursor.execute("""
                UPDATE streak
                SET count = ?, last_completed_date = ?
                WHERE habit_id = ? AND user_id = ?
            """, (count, today, habit_id, user_id))
        else:
            count = 1
            cursor.execute("""
                INSERT INTO streak (habit_id, user_id, count, last_completed_date)
                VALUES (?, ?, ?, ?)
            """, (habit_id, user_id, count, today))

        # Update the habit's last completed date
        cursor.execute("""
            UPDATE habits
            SET last_completed_at = ?
            WHERE habit_id = ? AND user_id = ?
        """, (completed_at, habit_id, user_id))

        conn.commit()  # Commit the transaction

    # Print confirmation and the total number of completions
    questionary.print(f"✅ Logged completion for Habit ID {habit_id}.")
    questionary.print(f"🔥 Total completions so far: {count}")


# ---------------------------
# Delete a habit
# ---------------------------
def delete_habit():
    # Prompt for username and password
    username = questionary.text("Enter your username:").ask()
    password = questionary.password("Enter your password:").ask()

    # Open a connection to the database and authenticate
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()

        # If authentication fails, print an error
        if not user:
            questionary.print("❌ Incorrect credentials.")
            return

        user_id = user[0]

        # Prompt for habit ID to delete
        habit_id = questionary.text("Enter the Habit ID to delete:").ask()

        # Check if the habit exists for the user
        cursor.execute("SELECT * FROM habits WHERE habit_id = ? AND user_id = ?", (habit_id, user_id))
        if not cursor.fetchone():
            questionary.print("⚠️ Habit not found or doesn't belong to you.")
            return

        # Confirm deletion before removing the habit
        confirm = questionary.confirm("⚠️ Confirm deletion of this habit?").ask()
        if confirm:
            cursor.execute("DELETE FROM habits WHERE habit_id = ? AND user_id = ?", (habit_id, user_id))
            conn.commit()  # Commit the deletion
            questionary.print(f"🗑️ Habit ID {habit_id} deleted successfully!")
        else:
            questionary.print("❎ Habit deletion cancelled.")


# ---------------------------
# View a user profile
# ---------------------------
def view_user_profile():
    # Prompt for username and password to authenticate
    username = questionary.text("Enter your username:").ask()
    password = questionary.password("Enter your password:").ask()

    # Open a connection to the database
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, username FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()

        # If no user is found, print an error
        if not user:
            questionary.print("❌ Invalid username or password.")
        else:
            # Print user profile information
            questionary.print("👤 User Profile:")
            questionary.print(f"ID: {user[0]}")
            questionary.print(f"Username: {user[1]}")


# ---------------------------
# Delete account
# ---------------------------
def delete_user():
    # Prompt for username and password to authenticate
    username = questionary.text("Enter your username:").ask()
    password = questionary.password("Enter your password:").ask()

    # Open a connection to the database
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()

        # If authentication fails, print an error
        if not user:
            questionary.print("❌ Invalid credentials.")
            return

        # Confirm deletion of the user's account and associated data
        confirm = questionary.confirm(
            "⚠️ Are you sure you want to delete your account and all associated habits?"
        ).ask()

        if confirm:
            cursor.execute("DELETE FROM users WHERE user_id = ?", (user[0],))
            conn.commit()  # Commit the deletion
            questionary.print("🗑️ Account deleted successfully.")
        else:
            questionary.print("❎ Account deletion canceled.")


# ---------------------------
# Main Menu Loop
# ---------------------------
def main():
    # Main menu loop for navigating through different options
    while True:
        choice = questionary.select(
            "🏠 Main Menu - Choose an option:",
            choices=[
                "Register",
                "View Profile",
                "Add Habit",
                "View Habits",
                "Log Habit Completion",
                "Delete Habit",
                "Delete Account",
                "Analytics",
                "Exit"
            ]
        ).ask()

        # Call respective functions based on the user's choice
        if choice == "Register":
            register()
        elif choice == "View Profile":
            view_user_profile()
        elif choice == "Add Habit":
            add_habit()
        elif choice == "View Habits":
            view_habit()
        elif choice == "Log Habit Completion":
            log_completion()
        elif choice == "Delete Habit":
            delete_habit()
        elif choice == "Delete Account":
            delete_user()
        elif choice == "Analytics":
            run_analytics()  # Run the analytics function
        elif choice == "Exit":
            # Exit the program
            questionary.print("👋 Goodbye!")
            break


if __name__ == '__main__':
    main()  # Run the main function to start the application
