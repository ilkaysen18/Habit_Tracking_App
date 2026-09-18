"""
TEST FIXTURE DATABASE (DB):

This is a separate DB for the Test Fixture of 4-Weeks Dummy Data for the 5 Predefined Habits.
"""



# Imports SQLite3 for the DB.
import sqlite3



# Definitions below.


def get_test_connection(db_name: str = "test_fixture.db"):
    return sqlite3.connect(db_name)


def initialize_test_tables(db_name: str = "test_fixture.db"):

    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()

        # Habits Table for the Test Fixtures.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_name STRING NOT NULL,
                periodicity STRING NOT NULL,
                created_at DATETIME NOT NULL,
                edited_at DATETIME NOT NULL
            );
        """)

        # Completion Logs Table for the Test Fixtures.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS completion_logs (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                completed_at DATETIME NOT NULL,
                FOREIGN KEY (habit_id) REFERENCES habits(habit_id)
            );
        """)

        # Must commit to finalize above details.
        conn.commit()
