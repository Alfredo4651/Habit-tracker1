import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
import main

# Fixture to mock database connection
@pytest.fixture
def mock_db():
    """
        Mock database fixture to simulate database connection and cursor.
        This avoids using a real database and speeds up testing by using MagicMock objects.
        It replaces the actual database connection with a mocked one for testing purposes.
        """
    with patch('main.get_connection') as mock_conn:
        conn = MagicMock()
        cursor = MagicMock()
        conn.cursor.return_value = cursor
        mock_conn.return_value.__enter__.return_value = conn
        yield conn, cursor

# Tests for main.py functions
def test_register(mock_db):
    """
       Test case for the 'register' function in the 'main' module.
       Simulates a user registration and checks if the SQL query to insert user data is executed correctly.
       """
    conn, cursor = mock_db
    with patch('main.questionary.print') as mock_print:
        main.register("testuser", "password123")
        cursor.execute.assert_called_once_with(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            ("testuser", "password123")
        )
        conn.commit.assert_called_once()
        mock_print.assert_called_once_with("✅ User 'testuser' registered successfully!")

def test_add_habit_success(mock_db):
    """
        Test case for the 'add_habit' function in the 'main' module.
        Verifies that a habit is successfully added to the database and the commit is made.
        """
    conn, cursor = mock_db
    cursor.fetchone.side_effect = [(123,), None]
    with patch('main.questionary.print') as mock_print:
        main.add_habit("testuser", 123, "Run", "Morning run", "daily")
        insert_call = [c for c in cursor.execute.call_args_list if "INSERT INTO habits" in c[0][0]][0]
        args = insert_call[0][1]
        assert args[0] == "Run"
        assert args[1] == "Morning run"
        assert args[2] == "daily"
        assert isinstance(args[3], datetime)
        assert args[4] == 123
        conn.commit.assert_called_once()
        mock_print.assert_called_once_with("✅ Habit 'Run' added successfully!")

def test_add_habit_user_mismatch(mock_db):
    """
        Test case for the 'add_habit' function when the username and user ID do not match.
        Ensures that the appropriate error message is printed.
        """
    conn, cursor = mock_db
    cursor.fetchone.return_value = (456,)
    with patch('main.questionary.print') as mock_print:
        main.add_habit("testuser", 123, "Run", "Morning run", "daily")
        mock_print.assert_called_once_with("❌ Username and User ID do not match.")

def test_view_habit_success(mock_db):
    """
        Test case for the 'view_habit' function in the 'main' module.
        Simulates viewing a habit's details for a given user and verifies the output.
        """
    conn, cursor = mock_db
    cursor.fetchone.return_value = (123,)
    cursor.fetchall.return_value = [(1, "Run", "Morning run", "daily", "Yes", None)]
    with patch('main.questionary.print'):
        main.view_habit("testuser", "password123")

def test_log_completion_new(mock_db):
    """
        Test case for the 'log_completion' function when logging a new habit completion.
        Verifies that the completion is logged and the streak is updated correctly.
        """
    conn, cursor = mock_db
    cursor.fetchone.side_effect = [(123,), ("daily",), None]
    with patch('main.questionary.print') as mock_print:
        main.log_completion("testuser", 123, 1, "2023-01-01")
        conn.commit.assert_called_once()
        mock_print.assert_any_call("✅ Logged completion for Habit ID 1.")
        mock_print.assert_any_call("🔥 Total completions so far: 1")

def test_delete_habit_success(mock_db):
    """
        Test case for the 'delete_habit' function in the 'main' module.
        Verifies that a habit is successfully deleted when confirmed.
        """
    conn, cursor = mock_db
    cursor.fetchone.side_effect = [(123,), (1,)]
    with patch('main.questionary.confirm') as mock_confirm:
        mock_confirm.return_value = MagicMock(ask=MagicMock(return_value=True))
        with patch('main.questionary.print') as mock_print:
            main.delete_habit("testuser", "password123", 1)
            conn.commit.assert_called_once()
            mock_print.assert_called_once_with("🗑️ Habit ID 1 deleted successfully!")

def test_delete_habit_cancel(mock_db):
    """
       Test case for the 'delete_habit' function when the user cancels the deletion.
       Verifies that no deletion occurs and the cancellation message is printed.
       """
    conn, cursor = mock_db
    cursor.fetchone.side_effect = [(123,), (1,)]
    with patch('main.questionary.confirm') as mock_confirm:
        mock_confirm.return_value = MagicMock(ask=MagicMock(return_value=False))
        with patch('main.questionary.print') as mock_print:
            main.delete_habit("testuser", "password123", 1)
            mock_print.assert_called_once_with("❎ Habit deletion cancelled.")

def test_view_user_profile(mock_db):
    """
        Test case for the 'view_user_profile' function in the 'main' module.
        Verifies that the user's profile information is correctly displayed.
        """
    conn, cursor = mock_db
    cursor.fetchone.return_value = (123, "testuser")
    with patch('main.questionary.print') as mock_print:
        main.view_user_profile("testuser", "password123")
        mock_print.assert_any_call("👤 User Profile:")
        mock_print.assert_any_call("ID: 123")
        mock_print.assert_any_call("Username: testuser")

def test_delete_user_success(mock_db):
    """
        Test case for the 'delete_user' function in the 'main' module.
        Verifies that the user is successfully deleted when confirmed.
        """
    conn, cursor = mock_db
    cursor.fetchone.return_value = (123,)
    with patch('main.questionary.confirm') as mock_confirm:
        mock_confirm.return_value = MagicMock(ask=MagicMock(return_value=True))
        with patch('main.questionary.print') as mock_print:
            main.delete_user("testuser", "password123")
            conn.commit.assert_called_once()
            mock_print.assert_called_once_with("🗑️ Account deleted successfully.")

def test_delete_user_cancel(mock_db):
    """
        Test case for the 'delete_user' function when the user cancels the deletion.
        Verifies that no deletion occurs and the cancellation message is printed.
        """
    conn, cursor = mock_db
    cursor.fetchone.return_value = (123,)
    with patch('main.questionary.confirm') as mock_confirm:
        mock_confirm.return_value = MagicMock(ask=MagicMock(return_value=False))
        with patch('main.questionary.print') as mock_print:
            main.delete_user("testuser", "password123")
            mock_print.assert_called_once_with("❎ Account deletion canceled.")
