"""
"COMPLETION LOG" CLASS - MODEL PACKAGE:
This Module defines the tracking timestamps regarding user habit completion and broken habits.
"""


from datetime import datetime


class CompletionLog:
  """
  This Class represents the habit logs.
  Attributes:
    log_id (int): PK - This Primary Key is the Log Class' (relational) unique identifier.
    habit_id (int): FK - This is the Foreign Key connecting back to the parent "Habit".
    completed_at (datetime): Metadata record for tracking the timestamp of habit completion.
    broken_at (datetime): Similar to above; tracks the time a habit was broken.
  """


def __init__(self, log_id: int, habit_id: int, completed_at: datetime, broken_at: datetime = None):
    """Initializes habit/task Attributes."""
    self.log_id = log_id
    self.habit_id = habit_id
    self.completed_at = completed_at
    self.broken_at = broken_at


"""Constraint Rules below:"""

def create_log(self, habit_id: int) -> None:
    """
    Function: Stub Method
        This preserves the architectural/design layout of the UML Class Diagram in the code.
        The function is empty for now; it will connect with the SQLLite Database Manager layer.
    """
    pass
