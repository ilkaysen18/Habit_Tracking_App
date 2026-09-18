"""
PREDEFINED HABITS:
These are the 5 Predefined Habits
- not specifically for Testing - rather, they are automatically displayed in the app when run for the first time after downloading.
"""


import sys
from datetime import datetime, timedelta
from database.db_manager import initialize_tables, seed_predefined_fixtures, get_connection
from models.habit import Habit
from models.completion_log import CompletionLog
from modules.analytics import (
    list_all_habits,
    filter_by_periodicity,
    get_longest_streak_one,
    get_longest_streak_all
)


