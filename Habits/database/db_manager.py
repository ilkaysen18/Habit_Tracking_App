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
    """Automates the 5 Predefined Test Fixtures and generates 4-Week Test Data."""
    with get_connection() as conn:
        cursor = conn.cursor()

    # Prevents duplication:
    cursor.execute("SELECT COUNT(*) FROM habits;")
      if cursor.fetchone()[0] > 0:
          return
      
      now = datetime.now()
      start_date = now - timedelta(weeks=4)

      # 1. Defines the 5 Data Records:
      predefined_habits = [
          ("Drink 2L water", "daily"),
          ("Go to the gym", "daily"),
          ("Read 10 pages", "daily"),
          ("Wash the car", "weekly"),
          ("Submit weekly timesheet", "weekly")
        ]

     for name, periodicity in predefined_habits:
          cursor.execute("""
              INSERT INTO habits (habit_name, periodicity, created_at, edited_at)
              VALUES (?, ?, ?, ?);
          """, (name, periodicity, start_date.strftime("%Y-%m-%d %H:%M:%S"), start_date.strftime("%Y-%m-%d %H:%M:%S")))
            
          habit_id = cursor.lastrowid

          # 2. Automates timestamp Data Block loops of 4 Weeks.
          current_log_date = start_date
          while current_log_date <= now:
              if periodicity == "daily":
                  # "Drink 2L water" includes a few gaps for Testing "streak" breaks/resets:
                  if name == "Go to the gym" and current_log_date.day % 7 in:
                      current_log_date += timedelta(days=1)
                      continue
                    
                  cursor.execute("""
                      INSERT INTO completion_logs (habit_id, completed_at)
                      VALUES (?, ?);
                  """, (habit_id, current_log_date.strftime("%Y-%m-%d %H:%M:%S")))
                  current_log_date += timedelta(days=1)
                
              elif periodicity == "weekly":
                  cursor.execute("""
                      INSERT INTO completion_logs (habit_id, completed_at)
                      VALUES (?, ?);
                  """, (habit_id, current_log_date.strftime("%Y-%m-%d %H:%M:%S")))
                  current_log_date += timedelta(weeks=1)
              
              elif periodicity == "biweekly":
                  current_log_date += timedelta(days=3)        # Standardizes biweekly as 3 days (considering biweekly is twice weekly).
              elif periodicity == "fortnightly":
                  current_log_date += timedelta(days=14)       # The standardized fortnightly time period of 14 days.
              elif periodicity == "monthly":
                  current_log_date += timedelta(days=30)       # Standardizes monthly as 30 days.
              elif periodicity == "yearly":
                  current_log_date += timedelta(days=365)      # The standardized yearly time period of 365 days.
              
      conn.commit()
