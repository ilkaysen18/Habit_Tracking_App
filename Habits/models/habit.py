"""
"HABIT" CLASS - MODEL PACKAGE:
This Module defines the Attributes for tracking user habits.
"""


from datetime import datetime, time


class Habit:
    """
    This Class represents the habits that users create to track their habits and/or tasks.
    Attributes:
      habit_id (int): PK - This Primary Key is the Habit Class' (relational) unique identifier.
      habit_name (str): This Attribute is for the habit/task's name.
      periodicity (str): frequency - 'daily', 'weekly', 'biweekly', 'fortnightly', 'monthly', 'yearly'.
      created_at (datetime): Metadata record for tracking the timestamp of habit creation.
      edited_at (datetime): Similar to above; tracks the time a habit was edited.
      reminder_time (time): A configuration that tracks user alerts.
    """

    def __init__(
        self,
        habit_id: int,
        habit_name: str,
        periodicity: str,
        created_at: datetime,
        edited_at: datetime,
        reminder_time=None
    ):
        """A tracking Container with Attributes for the "Habit" Class."""
        self.habit_id = habit_id
        self.habit_name = habit_name
        self.periodicity = periodicity
        self.created_at = created_at
        self.edited_at = edited_at
        self.reminder_time = reminder_time

    def edit_name(self, new_name: str) -> bool:
        """Modifies the title of the Attribute."""
        if new_name and len(new_name.strip()) > 0:
            self.habit_name = new_name.strip()
            self.edited_at = datetime.now()
            return True
        return False

    def edit_periodicity(self, new_periodicity: str) -> bool:
        """Updates the frequency of the habit/task."""
        valid_bounds = ["daily", "weekly", "biweekly", "fortnightly", "monthly", "yearly"]
        if new_periodicity in valid_bounds:
            self.periodicity = new_periodicity
            self.edited_at = datetime.now()
            return True
        return False

    def delete(self) -> bool:
        """Tracks individual habit/task deletion instances."""
        return True

    def complete(self) -> bool:
        """Tracks individual habit/task completion instances."""
        return True
