"""
Completion Log:

This  module holds the "CompletionLog" Class (or Entity). This Class tracks the individual
timestamps for users, regarding habit completion and broken habits.
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

def __init__(self, habit_id: int, habit_name: str, periodicity: str,
              created_at: datetime, edited_at: datetime, reminder_time: time = None):
    """A tracking Container with Attributes for the "Habit" Class."""
    self.habit_id = habit_id
    self.habit_name = habit_name
    self.periodicity = periodicity
    self.created_at = created_at
    self.edited_at = edited_at
    self.reminder_time = reminder_time
                
def edit_name(self, new_name: str) -> bool:
    """
    Modifies the title of the Attribute.
    Args:
        new_name (str): The updated habit/task title changed by the user.
    Returns:
        bool: True if input is valid and the text field is saved.
    """
    valid_bounds = ["daily", "weekly", "biweekly", "fortnightly", "monthly", "yearly"]
    
    








