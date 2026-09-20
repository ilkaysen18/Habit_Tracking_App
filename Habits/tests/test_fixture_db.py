"""
TEST FIXTURE DATABASE (DB):

This is a separate DB for the Test Fixture of 4-Weeks Dummy Data for the 5 Predefined Habits.
"""



# Imports SQLite3 for the DB.
import sqlite3
# Imports DATETIME for the Data Types.
from datetime import datetime, timedelta
# Imports Habits, CompletionLogs, and Analytics from (the general) Models and Modules.
from models.habit import Habit
from models.completion_log import CompletionLog
from modules.analytics import (
    list_all_habits,
    filter_by_periodicity,
    calculate_streak_for_single_habit,
    get_longest_streak_one,
    get_longest_streak_all
)



# Definitions below.


def get_test_connection(db_name: str = "test_fixture_db"):
    return sqlite3.connect(test_fixture_db)


def initialize_test_tables(test_fixture_db):

    with sqlite3.connect(test_fixture_db) as conn:
        cursor = conn.cursor()

        # Habits Table for the Test Fixtures.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Predefined_Habits_Test_Fix (
                habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_name STRING NOT NULL,
                periodicity STRING NOT NULL,
                created_at DATETIME NOT NULL,
                edited_at DATETIME NOT NULL
            );
        """)

        # Completion Logs Table for the Test Fixtures.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Completion_Logs_Test_Fix (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                completed_at DATETIME NOT NULL,
                FOREIGN KEY (habit_id) REFERENCES habits(habit_id)
            );
        """)

        # Must commit to finalize above details.
        conn.commit()
