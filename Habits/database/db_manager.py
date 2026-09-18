"""
DATABASE & TEST FIXTURE - MANAGEMENT LIBRARY:

This Module initializes the SQLite3 Relational Schema
and automates the 4-Week Test Tracking data.
"""


import sqlite3 
from datetime import datetime, timedelta

DB_PATH = "tracker.db"

def get_connection():
    """Initializes and returns connection instances to the SQLite Database."""
    return sqlite3.connect(DB_PATH)


def initialize_tables() -> None:
    """
    The raw DDL definitions for the Normalized Tables.
    PK & FK records are securely bound by their Entity/Class Constraints.
    """
    with get_connection() as conn:
        cursor = conn.cursor()

        # 1. Establishes the "Habits" Table Schema:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_name TEXT NOT NULL,
                periodicity TEXT NOT NULL,
                created_at TEXT NOT NULL,
                edited_at TEXT NOT NULL
            );
        """)

        # 2. Establishes the "Completion Logs" Table Schema - Connects Relational FK:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS completion_logs (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                completed_at TEXT NOT NULL,
                broken_at TEXT,
                FOREIGN KEY (habit_id) REFERENCES habits(habit_id) ON DELETE CASCADE
            );
        """)
        conn.commit()


def seed_predefined_fixtures() -> None:
    """Ensures the 5 Predefined Habits exist in the DB (no early return)."""

    with get_connection() as conn:
        cursor = conn.cursor()

        predefined_habits = [
            ("Drink 2L water", "daily"),
            ("Go to the gym", "daily"),
            ("Read 10 pages", "daily"),
            ("Wash the car", "weekly"),
            ("Submit weekly timesheet", "weekly")
        ]

        now = datetime.now()
        start_date = now - timedelta(weeks=4)
        now_str = now.strftime("%Y-%m-%d %H:%M:%S")
        start_str = start_date.strftime("%Y-%m-%d %H:%M:%S")

        for name, periodicity in predefined_habits:
            # Check if this predefined habit already exists
            cursor.execute("""
                SELECT habit_id
                FROM habits
                WHERE habit_name = ?
                    AND periodicity = ?
                LIMIT 1;
            """, (name, periodicity))

            existing = cursor.fetchone()
            if existing is not None:
                continue  # already exists; do not insert again

            # Insert missing habit
            cursor.execute("""
                INSERT INTO habits (habit_name, periodicity, created_at, edited_at)
                VALUES (?, ?, ?, ?);
            """, (name, periodicity, start_str, start_str))

        conn.commit()


def update_habit_name(habit_id: int, new_name: str) -> None:
    """Updates the habit_name for a given habit_id."""
    new_name = (new_name or "").strip()
    if not new_name:
        return

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE habits
            SET habit_name = ?, edited_at = ?
            WHERE habit_id = ?;
        """, (new_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), habit_id))
        conn.commit()


def update_habit_periodicity(habit_id: int, new_periodicity: str) -> None:
    """Updates the periodicity for a given habit_id."""
    valid_bounds = ["daily", "weekly", "biweekly", "fortnightly", "monthly", "yearly"]
    if not new_periodicity or new_periodicity.lower() not in valid_bounds:
        return

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE habits
            SET periodicity = ?, edited_at = ?
            WHERE habit_id = ?;
        """, (new_periodicity.lower(), datetime.now().strftime("%Y-%m-%d %H:%M:%S"), habit_id))
        conn.commit()
