"""
"HABIT TRACKER CLI" CLASS - MAIN GATEWAY FOR COMMAND LINE INTERFACE LAYER:

This Module holds the Menu loop and validates user input flows.
It connects the Database to the Analytics.
"""


import sys
from datetime import datetime
from database.db_manager import initialize_tables, seed_predefined_fixtures, get_connection
from models.habit import Habit
from models.completion_log import CompletionLog
from modules.analytics import (
    list_all_habits,
    filter_by_periodicity,
    get_longest_streak_one,
    get_longest_streak_all
)


def fetch_active_environment():
    """
    Queries SQLite3 Tables.
    Returns:
        tuple: (list of Habit Objects, list of CompletionLog Objects)
    """
    habits_cache = []
    logs_cache = []

    with get_connection() as conn:
        cursor = conn.cursor()

        # 1. Rehydrates (restores from memory) the Object-Oriented Design (OOD) "Habit" Objects:
        cursor.execute("SELECT habit_id, habit_name, periodicity, created_at, created_at FROM habits;")
        for row in cursor.fetchall():
            habits_cache.append(Habit(
                habit_id=row[0],
                habit_name=row[1],
                periodicity=row[2],
                created_at=datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S"),
                edited_at=datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S")
            ))

        # 2. Rehydrates the OOD "CompletionLog" Objects:
        cursor.execute("SELECT log_id, habit_id, completed_at FROM completion_logs;")
        for row in cursor.fetchall():
            logs_cache.append(CompletionLog(
                log_id=row[0],
                habit_id=row[1],
                completed_at=datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S")
            ))

    return habits_cache, logs_cache


def create_new_habit_flow() -> None:
    """ This is for handling the terminal prompt sequences - for the creation and saving of new habit/task records. """
    print("\n--- 🆕 CREATE A NEW HABIT ---")
    name = input("Enter a clear name/specification for the task: ").strip()
    if not name:
        print("❌ Invalid: Habit name cannot be empty.")
        return
    print("Choose Time Frame:")
    print("1. daily")
    print("2. weekly")
    print("3. biweekly")
    print("4. fortnightly")
    print("5. monthly")
    print("6. yearly")
    p_choice = input("Select choice code (1-6): ").strip()
    
    # Structural Block that converts Menu tokens to numbers for the Database:
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
        print("❌ Invalid input.")
        return















