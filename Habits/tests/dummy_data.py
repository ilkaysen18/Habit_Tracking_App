"""
DUMMY DATA: 

This file includes the Dummy Data Tables for the Test Fixtures, using SQLite3.


A HABITS TABLE & A COMPLETION LOGS TABLE for the Five Predefined Habits:

DATETIME was selected for created_at and edited_at. It ran a SyntaxError
(for leading zeros in decimal integer literals).
So it was changed to STRING instead, for the dummy_data only.
"""



# Imports SQLite3 for the Dummy Data Tables.
import sqlite3



def initialize_test_tables(db_name: str = "test_fixture_db"):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()

        cursor.execute(
            CREATE TABLE IF NOT EXISTS Predefined_Habits_Test_Fix (
                habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_name STRING NOT NULL,
                periodicity STRING NOT NULL,
                created_at STRING,
                edited_at STRING
            );
        )

        cursor.execute(
            CREATE TABLE IF NOT EXISTS Completion_Logs_Test_Fix (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                completed_at STRING,
                FOREIGN KEY (habit_id) REFERENCES Predefined_Habits_Test_Fix(habit_id)
            );
        )

        # Reset:
        cursor.execute("DELETE FROM Completion_Logs_Test_Fix;")
        cursor.execute("DELETE FROM Predefined_Habits_Test_Fix;")
        conn.commit()

        """HABITS TABLE for the Five Predefined Habits."""
        now_created = "19-07-26 07:00:00"
        habits = [
            ("Drink 2L water", "daily",   "19-07-26 07:08:05", None),
            ("Go to the gym",   "daily",   "19-07-26 07:09:42", None),
            ("Read 10 pages",  "daily",   "19-07-26 07:10:31", None),
            ("Wash the car",   "weekly",  "19-07-26 08:15:07", None),
            ("Submit weekly timesheet", "weekly", "19-07-26 08:17:28", None),
        ]

        cursor.executemany(
            INSERT INTO Predefined_Habits_Test_Fix (habit_name, periodicity, created_at, edited_at)
            VALUES (?, ?, ?, ?);
        , habits)

        """4 Weeks COMPLETION LOGS TABLE for Five Predefined Habits."""
        # completed_at for Broken Habits is left as NONE in Python for SQL's NULL.
        completion_rows = [
            (1, "19-07-26 12:56:40"), # First Predefined Habit.
            (1, "20-07-26 16:21:34"),
            (1, None),
            (1, None),
            (1, "23-07-26 16:02:54"),
            (1, "24-07-26 18:42:57"),
            (1, "25-07-26 17:30:24"),
            (1, None),
            (1, "27-07-26 15:55:23"),
            (1, "28-07-26 14:38:42"),
            (1, "28-07-26 14:43:55"),
            (1, "29-07-26 15:51:45"),
            (1, "30-07-26 13:12:25"),
            (1, "31-07-26 14:53:39"),
            (1, None),
            (1, "02-08-26 15:23:09"),
            (1, "03-08-26 19:25:56"),
            (1, "04-08-26 20:39:34"),
            (1, None),
            (1, None),
            (1, None),
            (1, "08-08-26 21:33:52"),
            (1, "09-08-26 22:30:23"),
            (1, "10-08-26 21:53:45"),
            (1, "11-08-26 23:38:12"),
            (1, "12-08-26 18:22:19"),
            (1, "13-08-26 19:34:38"),
            (1, "14-08-26 18:54:47"),
            (1, "15-08-26 23:27:58"),
            (2, None), # Second Predefined Habit.
            (2, None),
            (2, None),
            (2, None),
            (2, "23-07-26 21:04:37"), 
            (2, "24-07-26 21:08:29"),
            (2, None),
            (2, None),
            (2, None),
            (2, None),
            (2, None),
            (2, "30-07-26 21:05:15"),
            (2, None),
            (2, None),
            (2, None),
            (2, "03-08-26 21:31:23"),
            (2, None),
            (2, None),
            (2, "06-08-26 21:34:17"),
            (2, None),
            (2, None),
            (2, None),
            (2, "10-08-26 21:27:02"),
            (2, None),
            (2, None),
            (2, "13-08-26 21:40:08"),
            (2, None),
            (2, None),
            (3, "19-07-26 07:12:37"), # Third Predefined Habit.
            (3, "20-07-26 07:15:28"),
            (3, "21-07-26 07:10:03"),
            (3, "22-07-26 07:13:44"),
            (3, None),
            (3, None),
            (3, "25-07-26 07:16:51"),
            (3, "26-07-26 07:17:54"),
            (3, "27-07-26 07:11:34"),
            (3, "28-07-26 07:16:23"),
            (3, "29-07-26 07:18:54"),
            (3, "30-07-26 07:17:21"),
            (3, None),
            (3, "01-08-26 07:15:03"),
            (3, "02-08-26 07:13:08"),
            (3, "03-08-26 07:14:57"),
            (3, "04-08-26 07:17:43"),
            (3, "05-08-26 07:19:38"),
            (3, "06-08-26 07:21:29"),
            (3, "07-08-26 07:13:28"),
            (3, "08-08-26 07:15:37"),
            (3, "09-08-26 07:16:57"),
            (3, "10-08-26 07:14:44"),
            (3, "11-08-26 07:56:12"),
            (3, "12-08-26 07:15:17"),
            (3, "13-08-26 07:03:36"),
            (3, "14-08-26 07:04:57"),
            (3, "15-08-26 07:07:46"),
            (4, "23-07-26 06:37:24"), # Fourth Predefined Habit.
            (4, "30-07-26 06:28:16"),
            (4, "06-08-26 06:56:33"),
            (4, "13-08-26 06:30:52"),
            (5, "24-07-26 23:51:42"), # Fifth Predefined Habit.
            (5, "31-07-26 23:37:23"),
            (5, "07-08-26 22:43:13"),
            (5, "14-08-26 22:35:41"),
        ]

        cursor.executemany(
            INSERT INTO Completion_Logs_Test_Fix (habit_id, completed_at)
            VALUES (?, ?);
        , completion_rows)

        # Must commit to finalize above details.
        conn.commit()
