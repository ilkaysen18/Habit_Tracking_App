### Habit_Tracking_App

---------------------------------------------------

###### UML Class Diagram:
<img width="707" height="426" alt="UML Class Diagram" src="https://github.com/user-attachments/assets/527fe9fc-a974-4e15-9407-db0318b6e712" />

---------------------------------------------------

###### Navigation:
* [main.py](Habits/main.py) - This is for the "HabitTrackerCLI" Class; it includes the interactive Menu.
* [User Setup & Operation Manual](Habits/README.md) - This is for the Installation and Run Instructions.
* _database:_ [db_manager.py](Habits/database/db_manager.py) - This is the database (DB) integration for the SQLite3 connections.
* _models:_ [habit.py](Habits/models/habit.py) - This is for the main Object-Oriented Design (OOD) "Habit" Class.
* _models:_ [completion_log.py](Habits/models/completion_log.py) - This is for the "CompletionLog" Class.
* _modules:_ [analytics.py](Habits/modules/analytics.py) - This is for the "AnalyticsModule" Class; it includes the Python Functional Programming.
* _tests:_ [dummy_data.py](Habits/tests/dummy_data.py) - This consists of 5 Predefined Habits and includes their corresponding Dummy Data (SQLite Tables) for the Test Fixture.
* _tests:_ [test_fixture_db.py](Habits/tests/test_fixture_db.py) - This is a separate DB for the Test Fixture, as the dummy data doesn't belong in the main app DB.
