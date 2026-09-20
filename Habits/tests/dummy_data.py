"""
DUMMY DATA: 

This file includes the Dummy Data Tables for the Test Fixtures, using SQLite3.
"""



# Imports SQLite3 for the Dummy Data Tables.
import sqlite3
# Imports DATETIME for the Data Types.
from datetime import datetime



def initialize_test_tables(db_name: str = "test_fixture_db"):

    with sqlite3.connect(test_fixture_db) as conn:
        cursor = conn.cursor()

        """HABITS TABLE for the Five Predefined Habits."""
        cursor.execute(
            """
            DATETIME selected for created_at and edited_at.
            Ran a SyntaxError (for leading zeros in decimal integer literals).
            So changed it to STRING instead, for the dummy_data only.
            """
            CREATE TABLE Predefined_Habits_Test_Fix (habit_name STRING, periodicity STRING, created_at STRING, edited_at STRING)(
                ['Drink 2L water', 'daily', '19.07.26 07:08', NULL],
                ['Go to the gym', 'daily', '19.07.26 07:09', NULL],
                ['Read 10 pages', 'daily', '19.07.26 07:10', NULL],
                ['Wash the car', 'weekly', '19.07.26 08:15', NULL],
                ['Submit weekly timesheet', 'weekly', '19.07.26 08:17', NULL],
            );
        )

        """4 Weeks COMPLETION LOGS TABLE for Five Predefined Habits."""
        cursor.execute(
            CREATE TABLE Completion_Logs_Test_Fix (habit_id INTEGER, completed_at DATETIME)(
                [1, '19.07.26 12:56'], # First Predefined Habit.
                [1, '20.07.26 16:21'],
                [1, NULL],
                [1, NULL],
                [1, '23.07.26 16:02'],
                [1, '24.07.26 18:42'],
                [1, '25.07.26 17:30'],
                [1, NULL],
                [1, '27.07.26 15:55'],
                [1, '28.07.26 14:38'],
                [1, '29.07.26 15:36'],
                [1, '30.07.26 13:12'],
                [1, '31.07.26 14:46'],
                [1, NULL],
                [1, '02.08.26 15:23'],
                [1, '03.08.26 19:25'],
                [1, '04.08.26 20:39'],
                [1, NULL],
                [1, NULL],
                [1, NULL],
                [1, '08.08.26 21:33'],
                [1, '09.08.26 22:30'],
                [1, '10.08.26 21:53'],
                [1, '11.08.26 23:38'],
                [1, '12.08.26 18:22'],
                [1, '13.08.26 19:34'],
                [1, '14.08.26 18:54'],
                [1, '15.08.26 23:27'],
                [2, NULL], # Second Predefined Habit.
                [2, NULL],
                [2, NULL],
                [2, NULL],
                [2, '23.07.26 21:04'], 
                [2, '24.07.26 21:08'],
                [2, NULL],
                [2, NULL],
                [2, NULL],
                [2, NULL],
                [2, NULL],
                [2, '30.07.26 21:05'],
                [2, NULL],
                [2, NULL],
                [2, NULL],
                [2, '03.08.26 21:31'],
                [2, NULL],
                [2, NULL],
                [2, '06.08.26 21:34'],
                [2, NULL],
                [2, NULL],
                [2, NULL],
                [2, '10.08.26 21:27'],
                [2, NULL],
                [2, NULL],
                [2, '13.08.26 21:40'],
                [2, NULL],
                [2, NULL],
                [3, '19.07.26 07:12'], # Third Predefined Habit.
                [3, '20.07.26 07:15'],
                [3, '21.07.26 07:10'],
                [3, '22.07.26 07:13'],
                [3, NULL],
                [3, NULL],
                [3, '25.07.26 07:16'],
                [3, '26.07.26 07:17'],
                [3, '27.07.26 07:11'],
                [3, '28.07.26 07:16'],
                [3, '29.07.26 07:18'],
                [3, '30.07.26 07:17'],
                [3, NULL],
                [3, '01.08.26 07:15'],
                [3, '02.08.26 07:13'],
                [3, '03.08.26 07:14'],
                [3, '04.08.26 07:17'],
                [3, '05.08.26 07:19'],
                [3, '06.08.26 07:21'],
                [3, '07.08.26 07:13'],
                [3, '08.08.26 07:15'],
                [3, '09.08.26 07:16'],
                [3, '10.08.26 07:14'],
                [3, '11.08.26 07:56'],
                [3, '12.08.26 07:15'],
                [3, '13.08.26 07:03'],
                [3, '14.08.26 07:04'],
                [3, '15.08.26 07:07'],
                [4, '23.07.26 06:37'], # Fourth Predefined Habit.
                [4, '30.07.26 06:28'],
                [4, '06.08.26 06:56'],
                [4, '13.08.26 06:30'],
                [5, '24.07.26 23:51'], # Fifth Predefined Habit.
                [5, '31.07.26 23:37'],
                [5, '07.08.26 22:43'],
                [5, '14.08.26 22:35'],
            );
        )


# Must commit to finalize above details.
        conn.commit()
