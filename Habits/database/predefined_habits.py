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


def five_predefined_habits() -> None:
    """These are the 5 Predefined Habits."""
    with get_connection() as conn:
        cursor = conn.cursor()

    # Prevents duplication:
    cursor.execute("SELECT COUNT(*) FROM habits;")
    if cursor.fetchone()[0] > 0:
        return

    import sys
    from main import create_new_habit_flow

    period_specifications = {
        "1": "daily",
        "2": "weekly",
        "3": "biweekly",
        "4": "fortnightly",
        "5": "monthly",
        "6": "yearly"
    }

    periodicity = period_specifications.get(p_choice)
    if not periodicity:
        print("❌ Invalid periodicity choice.")
        return

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. Defines the 5 Data Records:
    predefined_habits = [
        ("Drink 2L water", "daily"),
        ("Go to the gym", "daily"),
        ("Read 10 pages", "daily"),
        ("Wash the car", "weekly"),
        ("Submit weekly timesheet", "weekly")
    ]

    for name, periodicity in five_predefined_habits:
        cursor.execute("""
            INSERT INTO habits (habit_name, periodicity, created_at, edited_at)
            VALUES (?, ?, ?, ?);
        """, (name, periodicity, start_date.strftime("%Y-%m-%d %H:%M:%S"), start_date.strftime("%Y-%m-%d %H:%M:%S")))
        habit_id = cursor.lastrowid
        conn.commit()
