"""
HABIT TRACKER CLI CLASS - MAIN GATEWAY FOR COMMAND LINE INTERFACE LAYER:

This Module holds the Menu loop and validates user input flows.
It connects the Database to the Analytics.
"""


#Imports Python's built-in library for its (operational) runtime commands:
import sys
# Imports calendar from datetime library, to generate timestamps and periodicity intervals/sequences:
from datetime import datetime, timedelta
# Imports from this repository (repo)'s own files; the Database (DB) folder's db_manager.py file:
from database.db_manager import (
    initialize_tables,
    seed_predefined_fixtures,
    get_connection,
    update_habit_name,
    update_habit_periodicity
) # Imports the individual Definitions/Functions inside the db_manager.py file.
# Imports other repo files, including - habit.py, completion_log.py, analytics.py:
from models.habit import Habit
from models.completion_log import CompletionLog
from modules.analytics import ( # Pulls the individual Definitions/Functions from the file:
    list_all_habits,
    filter_by_periodicity,
    get_longest_streak_one,
    get_longest_streak_all
)
# Imports the Test Fixture files from the repo;
# Renames/Aliases the initialize_test_tables Definition (def):
from tests.test_fixture_db import initialize_test_tables as initialize_test_schema
from tests.dummy_data import initialize_test_tables as initialize_test_data



""" Fetching environments from other files, including one for Test Fixtures:"""


def fetch_active_environment():
    """
    Queries SQLite3 Tables.
    Returns:
        tuple: (list of Habit Objects, list of CompletionLog Objects).
    """
    habits_cache = []
    logs_cache = []

    # Allows SQLite commands to be read/initialized by Python;
    # Considering the above Docstring within this Function (func) / def wouldn't be read otherwise.
    with get_connection() as conn:
        cursor = conn.cursor() # Pointer/Worker tool to execute SQL commands (within SQLite DB).

        # 1. Rehydrates (restores from memory) the Object-Oriented Design (OOD) "Habit" Objects:
        cursor.execute("""
            SELECT habit_id, habit_name, periodicity, created_at, edited_at
            FROM habits;
        """)
        for row in cursor.fetchall(): # Extracts data (rows, returned by SQL query); pulls data into a Python list.
            habits_cache.append(Habit( # Adds a new Habit Object to the active Habits cache (storage list).
                habit_id=row[0],
                habit_name=row[1],
                periodicity=row[2],
                created_at=datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S"),
                edited_at=datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S")
            ))
            # Note: DATETIME was changed to STRING for the Test Fixture.
            # This enabled more simplicity by preventing syntax/standardization errors,
            # when calling the data (SQL table rows).

        # 2. Rehydrates the OOD "CompletionLog" Objects:
        cursor.execute("SELECT log_id, habit_id, completed_at FROM completion_logs;")
        for row in cursor.fetchall():
            logs_cache.append(CompletionLog(
                log_id=row[0],
                habit_id=row[1],
                completed_at=datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S")
            ))

    return habits_cache, logs_cache # Returns the above (stored) data.


def fetch_test_fixture_environment_option_b(TEST_FIX_DB: str):
    """A loader for the Testing Database environment."""
    habits_cache = []
    logs_cache = []

    from tests.test_fixture_db import get_test_connection
    """This is known as a Helper Function, which supports other main function/s for Text Fixtures in this Module."""

    with get_test_connection(TEST_FIX_DB) as conn: 
        cursor = conn.cursor()

        # Fetches the 5 predefined habits for Test Fixture:
        cursor.execute("""
            SELECT habit_id, habit_name, periodicity, created_at, edited_at
            FROM Predefined_Habits_Test_Fix
        """)
        for row in cursor.fetchall(): 
            habits_cache.append(Habit(
                habit_id=row[0],
                habit_name=row[1],
                periodicity=row[2],
                created_at=datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S"),
                edited_at=datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S")
            ))

        cursor.execute("""
            SELECT log_id, habit_id, completed_at
            FROM Completion_Logs_Test_Fix;
        """)
        for row in cursor.fetchall():
            completed_at = row[2]
            # Since NULL/NONE was added for Broken Habits:
            if completed_at is None:
                continue
                # The Null/None data was cleaned from the DB later,
                # but the func is still kept here, for any future testing.

            logs_cache.append(CompletionLog(
                log_id=row[0],
                habit_id=row[1],
                completed_at=datetime.strptime(completed_at, "%Y-%m-%d %H:%M:%S")
            ))

    return habits_cache, logs_cache


"""The User Flow of the CLI is as follows:"""


def create_new_habit_flow(habits: list) -> None:
    """For the creation and saving of new habit/task records."""
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
    # These are the periodicity options for creating a new habit in the app.

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
        return # Returns a short error message if the user inputs an invalid periodicity selection.

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Saves the exact time the user created the new habit.

    # Inserts into the HABITS table - NOT completion_logs:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO habits (habit_name, periodicity, created_at, edited_at)
            VALUES (?, ?, ?, ?);
        """, (name, periodicity, now_str, now_str))
        conn.commit()

    print(f"✅ New habit saved: '{name}' set to {periodicity}.") # The saved habit is printed to confirm.


def check_off_habit_flow(habits: list) -> None:
    """For the completion of habit/tasks."""
    print("\n--- ✅ CHECK-OFF A HABIT OR TASK ---")

    if not habits:
        print("❌ No current tracking filters found.")
        return

    # 1. Defines the 5 Data Records:
    five_predefined_habits = [
        ("Drink 2L water", "daily"),
        ("Go to the gym", "daily"),
        ("Read 10 pages", "daily"),
        ("Wash the car", "weekly"),
        ("Submit weekly timesheet", "weekly")
    ]

    # Lists the 5 Predefined Habits:
    list(five_predefined_habits)

    # Builds a list of habits that are NOT completed yet (for the current period):
    with get_connection() as conn:
        available = [
            h for h in habits
            if not completed_habits(h.habit_id, h.periodicity)
        ]

    if not available:
        print("✅ All habits are already completed for the current period.")
        return

    for idx, h in enumerate(available): # Pairs Objects with counting indices starting at 0.
        print(f"{idx + 1}. {h.habit_name} [{h.periodicity}]")

    try:
        selection = int(input("\nSelect habit index row to complete: ")) - 1
        if selection < 0 or selection >= len(available):
            raise IndexError

        target_habit = available[selection]
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO completion_logs (habit_id, completed_at)
                VALUES (?, ?);
            """, (target_habit.habit_id, now_str))
            conn.commit()

        print(f"🎯 Milestone saved! '{target_habit.habit_name}' checked off at {now_str}.")
        # Habit Completion is checked off by user and confirmed by the system.

    except (ValueError, IndexError):
        print("❌ Interface Exception: Invalid option coordinates selected.")


"""
This is for habits that have already been checked-off as completed by the user,
so that they do not remain in the current habits list.
"""

def completed_habits(habit_id: int, periodicity: str) -> bool:
    now = datetime.now()
    p = periodicity.lower()

    if p == "daily":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)

    elif p == "weekly":
        # Week window: Monday 00:00 to next Monday 00:00.
        start = now - timedelta(days=now.weekday())
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(weeks=1)

    elif p == "biweekly" or p == "fortnightly":
        # Treats both as 2-week windows; set to the start of the current week (Monday).
        week_start = now - timedelta(days=now.weekday())
        week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)

        # Aligned to an even 2-Week block, based on fixed (anchor) date.
        anchor = datetime(2020, 1, 6)  # Monday
        anchor = anchor.replace(hour=0, minute=0, second=0, microsecond=0)

        weeks_since_anchor = (week_start - anchor).days // 7
        current_block_start = week_start - timedelta(weeks=weeks_since_anchor % 2)
        start = current_block_start
        end = start + timedelta(weeks=2)

    elif p == "monthly":
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        # Move to first day of next month.
        if now.month == 12:
            end = now.replace(year=now.year + 1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            end = now.replace(month=now.month + 1, day=1, hour=0, minute=0, second=0, microsecond=0)

    elif p == "yearly":
        start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        end = start.replace(year=start.year + 1)

    else:
        # Unknown periodicity is treated as NOT Completed.
        return False

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 1
            FROM completion_logs
            WHERE habit_id = ?
            AND completed_at >= ?
            AND completed_at < ?
            LIMIT 1;
        """, (habit_id, start.strftime("%Y-%m-%d %H:%M:%S"), end.strftime("%Y-%m-%d %H:%M:%S")))

    return cursor.fetchone() is not None


def edit_habit_flow(habits: list) -> None:
    """Edit a habit's name or periodicity from the CLI."""
    if not habits:
        print("❌ No habits available to edit.")
        return

    print("\n--- ✏️ EDIT A HABIT ---")
    for idx, h in enumerate(habits):
        print(f"{idx + 1}. ID {h.habit_id}: {h.habit_name} [{h.periodicity}]")

    try:
        sel = int(input("\nSelect habit index to edit: ")) - 1
        if sel < 0 or sel >= len(habits):
            raise IndexError
        target = habits[sel]
    except (ValueError, IndexError):
        print("❌ Selection out of operational bounds.")
        return

    print("\nEdit what?") # Displays the options to select for editing:
    print("1. Edit habit name")
    print("2. Edit habit periodicity")
    choice = input("Select option (1-2): ").strip()

    if choice == "1":
        new_name = input("Enter new habit name: ").strip()
        if not new_name:
            print("❌ Habit name cannot be empty.")
            return
        update_habit_name(target.habit_id, new_name)
        print(f"✅ Updated habit name to: '{new_name}'") # Displays the new name.

    elif choice == "2": # Displays the options for editing a habit by its periodicity:
        print("Choose Time Frame:")
        print("1. daily")
        print("2. weekly")
        print("3. biweekly")
        print("4. fortnightly")
        print("5. monthly")
        print("6. yearly")
        p_choice = input("Select choice code (1-6): ").strip()

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

        update_habit_periodicity(target.habit_id, periodicity)
        print(f"✅ Updated periodicity to: {periodicity}") # Updates, then displays the new periodicity confirmation message.

    else:
        print("❌ Invalid option.")


def run_analytics_dashboard(habits: list, logs: list):
    filtered = None
    """Functional Analytics Queries to analyze user progress."""
    while True:
        print("\n=== 📊 FUNCTIONAL ANALYTICS FILTERS ===")
        print("1. List All Currently Tracked Habits")
        print("2. Filter Habits by Periodicity Bounds")
        print("3. View Longest Completion Run Streak Across All Habits")
        print("4. View Longest Completion Run Streak for One Specific Habit")
        print("5. Return to Application Main Menu")
        # A list of all the Analytics Functions the user can choose from.

        choice = input("\nSelect analytics filter (1-5): ").strip()

        if choice == "1":
            all_h = list_all_habits(habits)
            print("\n📋 MASTER TRACKING REGISTRY:") # This lists all the current habits:
            for h in all_h:
                print(f" • ID {h.habit_id}: {h.habit_name} ({h.periodicity})")

        elif choice == "2": # Filters all current habits by periodicity:
            valid_filters = ["daily", "weekly", "biweekly", "fortnightly", "monthly", "yearly"]
            print("\nAvailable filters: " + ", ".join(valid_filters))

            p = input("Enter frequency: ").strip().lower()

            if p in valid_filters:
                filtered = filter_by_periodicity(habits, p)

                print(f"\n🔎 ONLY SHOWING {p.upper()} TRACKERS:")
            if not filtered:
                print("❌ No habits found matching this timeframe.")
            else:
                for h in filtered:
                    print(f" • {h.habit_name}")

        elif choice == "3": # Filters historical habits by longest completion streak for all habits:
            top_habit, top_run = get_longest_streak_all(habits, logs)

            if not top_habit:
                print("❌ No streak data available.")
            else:
                print(
                    f"🏆 Absolute Longest System-Wide Streak: "
                    f"{top_run} consecutive periods for '{top_habit.habit_name}'."
                )

        elif choice == "4": # Filters historical habits by longest completion streak PER habit selection:
            if not habits:
                print("❌ No rows available to verify.")
                continue
            for idx, h in enumerate(habits): # Lists the habits for the user to select:
                print(f"{idx + 1}. {h.habit_name} [{h.periodicity}]")
            try:
                sel = int(input("\nSelect habit index code: ")) - 1
                if sel < 0 or sel >= len(habits):
                    raise IndexError
                target = habits[sel]
                streak = get_longest_streak_one(target.habit_id, logs, target.periodicity)
                print(f"\n🎯 Max consecutive streak for '{target.habit_name}': {streak} periods.")
            except (ValueError, IndexError):
                print("❌ Selection out of operational bounds.")

        elif choice == "5": # Returns user to the app's MAIN Menu.
            break


"""This runs the Test Fixture for the user, by fetching the data stored in the SQLite DB."""
def run_test_fixture_4_weeks() -> None:
    print("\n📁 Test Fixture: 4-Weeks Dummy Data.")

    # Five Predefined Habits:
    predefined_habits = [
        ("Drink 2L water", "daily"),
        ("Go to the gym", "daily"),
        ("Read 10 pages", "daily"),
        ("Wash the car", "weekly"),
        ("Submit weekly timesheet", "weekly"),
    ]

    # 4-Weeks Dummy Data:
    now = datetime.now()

    # "Full" 28-day daily habits sequence:
    all_daily_dates = [
        now - timedelta(days=i)
        for i in range(27, -1, -1)]

    # "Gapped" 28-day daily habits sequence:
    # Based on completed habits vs broken habits - this tests Streak Analytics:

    daily_habit_dates = {

        "Drink 2L water": [
            d for i, d in enumerate(all_daily_dates)
            if i not in {5, 6, 15} # Example gaps for days habits were broken.
        ],

        "Go to the gym": [
            d for i, d in enumerate(all_daily_dates)
            if i not in {8, 9, 18, 19} # Example gaps for days habits are broken.
        ],

        "Read 10 pages": [
            d for i, d in enumerate(all_daily_dates)
            if i not in {3, 12, 13, 22} # Example gaps for days habits are broken.
        ],
    }

    # 4 weeks for weekly habits:
    weekly_dates = [
        now - timedelta(weeks=i)
        for i in range(3, -1, -1)
    ]

    # Imports Test Fixture Database (DB) - which is a separate DB specifically for the Test Fixture:
    from tests.test_fixture_db import (
        get_test_connection,
        initialize_test_tables,
    )

    TEST_FIX_DB = "test_fixture.db"

    # Ensures tables exist in the Test DB:
    initialize_test_tables(TEST_FIX_DB)

    with get_test_connection(TEST_FIX_DB) as conn:
        cursor = conn.cursor()

        # Clears Fixture Data so re-running doesn't duplicate:
        cursor.execute("DELETE FROM Predefined_Habits_Test_Fix;")
        cursor.execute("DELETE FROM Completion_Logs_Test_Fix;")
        conn.commit()

        # Inserts into Test Habits using IDs:
        habit_id_tests = {}
        now_str = now.strftime("%Y-%m-%d %H:%M:%S")

        for name, periodicity in predefined_habits:
            cursor.execute("""
                INSERT INTO Predefined_Habits_Test_Fix (habit_name, periodicity, created_at, edited_at)
                VALUES (?, ?, ?, ?);
            """, (name, periodicity, now_str, now_str))
            habit_id_tests[(name, periodicity)] = cursor.lastrowid

        conn.commit()

        # Inserts into Test Completion Logs:
        for name, periodicity in predefined_habits:
            habit_id = habit_id_tests[(name, periodicity)]

            if periodicity == "daily":
                dates_to_insert = daily_habit_dates[name]
            else:
                dates_to_insert = weekly_dates

            for d in dates_to_insert:
                cursor.execute("""
                    INSERT INTO Completion_Logs_Test_Fix (habit_id, completed_at)
                    VALUES (?, ?);
                """, (habit_id, d.strftime("%Y-%m-%d %H:%M:%S")))

        conn.commit()

    print("✅ Test Fixture has been added.")
    # Confirms the Test Fixture is ready for filtering (via the Test Fixture Analytics Dashboard).


"""
This is the Analytics Dashboard for the Test Fixture:
It is separate from the general Habits Analytics Dashboard.

Despite both dashboards including the same 5 predefined habits,
the 2 separate dashboards ensure that the Test Fixture Analytics contains
separate Completion Records, based on its relevant Dummy Data (SQL table rows).
"""

def run_test_fixture_analytics_dashboard(TEST_FIX_DB: str):
    while True:
        print("\n=== 📊 FUNCTIONAL ANALYTICS DASHBOARD (TEST FIXTURE) ===")
        print("1. List All Currently Tracked Habits")
        print("2. Filter Habits by Periodicity Bounds")
        print("3. View Longest Completion Run Streak Across All Habits")
        print("4. View Longest Completion Run Streak for One Specific Habit")
        print("5. Return to Application Main Menu")
        # Includes the exact same structure as the general Habits Analytics Dashboard.

        choice = input("\nSelect analytics option (1-5): ").strip()

        Predefined_Habits_Test_Fix, Completion_Logs_Test_Fix = \
            fetch_test_fixture_environment_option_b(TEST_FIX_DB)
            # Fetches the Test Fixture from memory.

        if choice == "1": # Lists all current (predefined) habits (as expected):
            all_h = list_all_habits(Predefined_Habits_Test_Fix)
            print("\n📋 TEST FIXTURE MASTER TRACKING REGISTRY:")
            for h in all_h:
                print(f" • ID {h.habit_id}: {h.habit_name} ({h.periodicity})")

        elif choice == "2": # Allows user to select historical Dummy habit-completions by periodicity:
            valid_filters = ["daily", "weekly", "biweekly", "fortnightly", "monthly", "yearly"]
            print("\nAvailable filters: " + ", ".join(valid_filters))
            p = input("Enter frequency: ").strip().lower()

            if p in valid_filters:
                filtered = filter_by_periodicity(Predefined_Habits_Test_Fix, p)
                print(f"\n🔎 ONLY SHOWING {p.upper()} TRACKERS:")

                if not filtered:
                    print("❌ No habits found matching this timeframe.")
                else:
                    for h in filtered:
                        print(f" • {h.habit_name}")
            else:
                print("❌ Invalid frequency input.")

        elif choice == "3": # Lists all historical habits from the Dummy data Rows:
            print(f"Total logs loaded = {len(Completion_Logs_Test_Fix)}") # The total Completed Logs for all the dummy data records.

            for log in Completion_Logs_Test_Fix:
                print( # Prints the total Completed Logs - listing each dummy record for: log_id, habit_id, & completed_at attributes:
                    f"log_id={log.log_id}, " 
                    f"habit_id={log.habit_id}, "
                    f"completed_at={log.completed_at}"
                )

            top_habit, top_run = get_longest_streak_all( # Calculates/Finds the Longest-Completion-Streak for the Dummy records.
                Predefined_Habits_Test_Fix,
                Completion_Logs_Test_Fix
            )
            if not top_habit:
                print("❌ No streak data available.")
            else:
                print( # Prints the Longest-Completion-Streak for Dummy records.
                    f"🏆 The Longest Streak for Test Fixtures: "
                    f"{top_run} consecutive periods for '{top_habit.habit_name}'."
                )

        elif choice == "4": # Similar to option 3, while allowing user to make a selection from the predefined habits:
            if not Predefined_Habits_Test_Fix:
                print("❌ No rows available to verify.")
                continue

            for idx, h in enumerate(Predefined_Habits_Test_Fix):
                print(f"{idx + 1}. {h.habit_name} [{h.periodicity}]")

            try:
                sel = int(input("\nSelect habit index code: ")) - 1
                if sel < 0 or sel >= len(Predefined_Habits_Test_Fix):
                    raise IndexError

                target = Predefined_Habits_Test_Fix[sel]
                streak = get_longest_streak_one(
                    target.habit_id,
                    Completion_Logs_Test_Fix,
                    target.periodicity
                )

                # Finds and prints the Longest-Completion-Streak (from Dummy records),
                # for the user-selected Habit choice. 

                print(f"\n🎯 The Longest Test Streak for '{target.habit_name}': {streak} periods.")
            except (ValueError, IndexError):
                print("❌ Selection is out of operational bounds.")

        elif choice == "5": # Returns to main Menu.
            break

        else:
            print("❌ Input Error: Unrecognized instruction.")


def main():
    """This initializes the system files along with the Test Fixtures and hosts the CLI Menu loop."""
    # Ensures Database structures and Test Fixtures are verified when launching the application:
    initialize_tables()
    seed_predefined_fixtures()

    while True:
        # Rehydrates (restores from memory) Object caches and maintains real-time sync:
        habits, logs = fetch_active_environment()

        # Prints the interactive Menu as a list for the user to select (from given options):
        print("\n=== 📋 MAIN INTERACTIVE APP MENU ===")
        print("1. Create a New Custom Habit Track")
        print("2. Mark a Habit Task as Completed")
        print("3. Open Functional Analytics Dashboard")
        print("4. Edit an Existing Habit by Name or Periodicity)")
        print("5. Terminate State Machine & Exit")
        print("6. Test Fixture for 4-Weeks Dummy Data (NOTE: must select this before option number seven!)")
        print("7. Analytics Dashboard for Test Fixture")
        # Note: User to select Option_6 prior to Option_7;
        # Since Option_6 fetches the dummy data from DB, initializing them in the app;
        # While Option_7 allows user to apply the Functional Analytics (to filter the dummy data).

        choice = input("\nSelect option coordinate (1-7): ").strip()

        if choice == "1":
            create_new_habit_flow(habits)
        elif choice == "2":
            check_off_habit_flow(habits)
        elif choice == "3":
            run_analytics_dashboard(habits, logs)
        elif choice == "4":
            edit_habit_flow(habits)
        elif choice == "5":
            print("\nProgress saved to local storage. Closing runtime loop. See you again soon!")
            sys.exit()
        elif choice == "6":
            run_test_fixture_4_weeks()
        elif choice == "7":
            TEST_FIX_DB = "test_fixture.db"
            initialize_test_schema(TEST_FIX_DB)
            run_test_fixture_analytics_dashboard(TEST_FIX_DB)
        else:
            print("❌ Input Error: Unrecognized instruction. Please choose options 1-7.")

if __name__ == "__main__":
    main()
    # The user can now open the CLI Menu on a shell (by typing a command prompt in the shell);
    # The user can navigate the interactive Menu by following the CLI prompt messages.
