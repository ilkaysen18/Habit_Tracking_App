"""
"COMPLETION LOG" CLASS - MODEL PACKAGE:
This Module defines the tracking timestamps for user habit completions and broken habits.
"""


from datetime import datetime


class CompletionLog:
    """
    This Class represents the habit logs.
    Attributes:
      log_id (int): PK - Primary Key.
      habit_id (int): FK - Foreign Key to Habit.
      completed_at (datetime): timestamp of completion.
      broken_at (datetime): timestamp of breaking (optional).
    """

    def __init__(
        self,
        log_id: int,
        habit_id: int,
        completed_at: datetime,
        broken_at: datetime = None
    ):
        """Initializes habit/task Attributes."""
        self.log_id = log_id
        self.habit_id = habit_id
        self.completed_at = completed_at
        self.broken_at = broken_at

    def create_log(self, habit_id: int) -> None:
        """Stub method (which connects to DB later)."""
        pass
