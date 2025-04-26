class User:
    """Represents a registered user in the habit tracker app.

    Attributes:
        user_id (int): Unique identifier for the user (primary key).
        username (str): The user's chosen username (must be unique).
        password (str): The user's password.
        created_at (str, optional): Timestamp when the user account was created.
    """

    def __init__(self, user_id, username, password, created_at=None):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.created_at = created_at


class Habit:
    """Represents a habit being tracked by a user.

    Attributes:
        habit_id (int): Unique identifier for the habit (primary key).
        user_id (int): ID of the user who owns this habit (foreign key).
        name (str): Name/title of the habit.
        description (str): A brief description of the habit's purpose.
        periodicity (str): Frequency of the habit ('daily' or 'weekly').
        created_at (str): Timestamp when the habit was created.
        is_active (str): Status of the habit ('Yes' for active, 'No' for inactive).
        last_completed_at (str, optional): Timestamp of the last completion of the habit.
    """

    def __init__(self, habit_id, user_id, name, description, periodicity, created_at, is_active='Yes',
                 last_completed_at=None):
        self.habit_id = habit_id
        self.user_id = user_id
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.created_at = created_at
        self.is_active = is_active
        self.last_completed_at = last_completed_at


class Streak:
    """Tracks a user's streaks for a particular habit (consecutive completions).

    Attributes:
        streak_id (int): Unique identifier for the streak record (primary key).
        habit_id (int): ID of the associated habit (foreign key).
        user_id (int): ID of the user who owns this streak.
        count (int): Number of consecutive successful completions.
        last_completed_date (str): Date when the habit was last completed.
    """

    def __init__(self, streak_id, habit_id, user_id, count, last_completed_date):
        self.streak_id = streak_id
        self.habit_id = habit_id
        self.user_id = user_id
        self.count = count
        self.last_completed_date = last_completed_date
