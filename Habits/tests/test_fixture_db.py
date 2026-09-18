"""
TEST FIXTURE DATABASE (DB):

This is a separate DB for the Test Fixture of 4-Weeks Dummy Data for the 5 Predefined Habits.
"""



import sqlite3

def get_test_connection(db_name: str = "test_fixture.db"):
    return sqlite3.connect(db_name)

def initialize_test_tables(db_name: str = "test_fixture.db"):

    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()

        # IMPORTANT:
        # Replace these table definitions with THE SAME DATA TYPES AS MAIN DB.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_name TEXT NOT NULL,
                periodicity TEXT NOT NULL,
                created_at TEXT NOT NULL,
                edited_at TEXT NOT NULL
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS completion_logs (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                completed_at TEXT NOT NULL,
                FOREIGN KEY (habit_id) REFERENCES habits(habit_id)
            );
        """)

        conn.commit()
