"""
HABIT TRACKER CLI CLASS - MAIN GATEWAY FOR COMMAND LINE INTERFACE LAYER:

This Module holds the Menu loop and validates user input flows.
It connects the Database to the Analytics.
"""



import sys
from datetime import datetime, timedelta
from database.db_manager import (
    initialize_tables,
    seed_predefined_fixtures,
    get_connection,
    update_habit_name,
    update_habit_periodicity
)
from models.habit import Habit
from models.completion_log import CompletionLog
from modules.analytics import (
    list_all_habits,
    filter_by_periodicity,
    get_longest_streak_one,
    get_longest_streak_all
)
from tests.test_fixture_db import initialize_test_tables as initialize_test_schema
from tests.dummy_data import initialize_test_tables as initialize_test_data



""" Fetching environments from other files, including one for Test Fixtures:"""


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
        cursor.execute("""
            SELECT habit_id, habit_name, periodicity, created_at, edited_at
            FROM habits;
        """)
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


def fetch_test_fixture_environment_option_b(TEST_DB_NAME: str):
    """A loader for the Testing Database environment."""
    habits_cache = []
    logs_cache = []

    from tests.test_fixture_db import get_test_connection
    """This is known as a Helper Function, which supports other main function/s for Text Fixtures in this Module."""

    with get_test_connection(TEST_DB_NAME) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT habit_id, habit_name, periodicity, created_at, edited_at
            FROM Predefined_Habits_Test_Fix;
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

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Insert into the HABITS table (NOT completion_logs)
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO habits (habit_name, periodicity, created_at, edited_at)
            VALUES (?, ?, ?, ?);
        """, (name, periodicity, now_str, now_str))
        conn.commit()

    print(f"✅ New habit saved: '{name}' set to {periodicity}.")


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

    # List the 5 Predefined Habits
    list(five_predefined_habits)

    # Build a list of habits that are NOT completed yet "for the current period"
    with get_connection() as conn:
        available = [
            h for h in habits
            if not completed_habits(h.habit_id, h.periodicity)
        ]

    if not available:
        print("✅ All habits are already completed for the current period.")
        return

    for idx, h in enumerate(available):
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

    except (ValueError, IndexError):
        print("❌ Interface Exception: Invalid option coordinates selected.")


def completed_habits(habit_id: int, periodicity: str) -> bool:
    now = datetime.now()
    p = periodicity.lower()

    if p == "daily":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)

    elif p == "weekly":
        # week window: Monday 00:00 to next Monday 00:00
        start = now - timedelta(days=now.weekday())
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(weeks=1)

    elif p == "biweekly" or p == "fortnightly":
        # treat both as 2-week windows; anchor to the start of the current week (Monday)
        week_start = now - timedelta(days=now.weekday())
        week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)

        # align to an even 2-week block relative to a fixed anchor date
        anchor = datetime(2020, 1, 6)  # Monday
        anchor = anchor.replace(hour=0, minute=0, second=0, microsecond=0)

        weeks_since_anchor = (week_start - anchor).days // 7
        current_block_start = week_start - timedelta(weeks=weeks_since_anchor % 2)
        start = current_block_start
        end = start + timedelta(weeks=2)

    elif p == "monthly":
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        # move to first day of next month
        if now.month == 12:
            end = now.replace(year=now.year + 1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            end = now.replace(month=now.month + 1, day=1, hour=0, minute=0, second=0, microsecond=0)

    elif p == "yearly":
        start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        end = start.replace(year=start.year + 1)

    else:
        # Unknown periodicity => treat as not completed
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

    print("\nEdit what?")
    print("1. Edit habit name")
    print("2. Edit habit periodicity")
    choice = input("Select option (1-2): ").strip()

    if choice == "1":
        new_name = input("Enter new habit name: ").strip()
        if not new_name:
            print("❌ Habit name cannot be empty.")
            return
        update_habit_name(target.habit_id, new_name)
        print(f"✅ Updated habit name to: '{new_name}'")

    elif choice == "2":
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
        print(f"✅ Updated periodicity to: {periodicity}")

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

        choice = input("\nSelect analytics filter (1-5): ").strip()

        if choice == "1":
            all_h = list_all_habits(habits)
            print("\n📋 MASTER TRACKING REGISTRY:")
            for h in all_h:
                print(f" • ID {h.habit_id}: {h.habit_name} ({h.periodicity})")

        elif choice == "2":
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

        elif choice == "3":
            top_habit, top_run = get_longest_streak_all(habits, logs)

            if not top_habit:
                print("❌ No streak data available.")
            else:
                print(
                    f"🏆 Absolute Longest System-Wide Streak: "
                    f"{top_run} consecutive periods for '{top_habit.habit_name}'."
                )

        elif choice == "4":
            if not habits:
                print("❌ No rows available to verify.")
                continue
            for idx, h in enumerate(habits):
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

        elif choice == "5":
            break


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

    # 28 days for daily habits:
    daily_dates = [now - timedelta(days=i) for i in range(27, -1, -1)]

    # 4 weeks for weekly habits:
    weekly_dates = [now - timedelta(weeks=i) for i in range(3, -1, -1)]

    # Imports Test Fixture Database (DB) - which is a separate DB specifically for the Test Fixture:
    from tests.test_fixture_db import (
        get_test_connection,
        initialize_test_tables,
    )

    TEST_DB_NAME = "test_fixture.db"

    # Ensures tables exist in the Test DB:
    initialize_test_tables(TEST_DB_NAME)

    with get_test_connection(TEST_DB_NAME) as conn:
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
            
            cursor.execute("""
                INSERT INTO Completion_Logs_Test_Fix (habit_id, completed_at)
                VALUES (?, ?);
            """, (habit_id, d.strftime("%Y-%m-%d %H:%M:%S")))

        conn.commit()

    print("✅ Test Fixture has been added.")


def run_test_fixture_analytics_dashboard(TEST_DB_NAME: str):
    while True:
        print("\n=== 📊 FUNCTIONAL ANALYTICS DASHBOARD (TEST FIXTURE) ===")
        print("1. List All Currently Tracked Habits")
        print("2. Filter Habits by Periodicity Bounds")
        print("3. View Longest Completion Run Streak Across All Habits")
        print("4. View Longest Completion Run Streak for One Specific Habit")
        print("5. Return to Application Main Menu")

        choice = input("\nSelect analytics option (1-5): ").strip()

        Predefined_Habits_Test_Fix, Completion_Logs_Test_Fix = \
            fetch_test_fixture_environment_option_b(TEST_DB_NAME)

        if choice == "1":
            all_h = list_all_habits(Predefined_Habits_Test_Fix)
            print("\n📋 TEST FIXTURE MASTER TRACKING REGISTRY:")
            for h in all_h:
                print(f" • ID {h.habit_id}: {h.habit_name} ({h.periodicity})")

        elif choice == "2":
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

        elif choice == "3":
            top_habit, top_run = get_longest_streak_all(
                Predefined_Habits_Test_Fix,
                Completion_Logs_Test_Fix
            )
            if not top_habit:
                print("❌ No streak data available.")
            else:
                print(
                    f"🏆 The Longest Streak for Test Fixtures: "
                    f"{top_run} consecutive periods for '{top_habit.habit_name}'."
                )

        elif choice == "4":
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

                print(f"\n🎯 The Longest Test Streak for '{target.habit_name}': {streak} periods.")
            except (ValueError, IndexError):
                print("❌ Selection is out of operational bounds.")

        elif choice == "5":
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

        print("\n=== 📋 MAIN INTERACTIVE APP MENU ===")
        print("1. Create a New Custom Habit Track")
        print("2. Mark a Habit Task as Completed")
        print("3. Open Functional Analytics Dashboard")
        print("4. Edit an Existing Habit (Name / Periodicity)")
        print("5. Terminate State Machine & Exit")
        print("6. Test Fixture (4-Weeks Dummy Data)")
        print("7. Analytics Dashboard for Test Fixture")

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
            TEST_DB_NAME = "test_fixture.db"
            initialize_test_schema(TEST_DB_NAME)
            run_test_fixture_analytics_dashboard(TEST_DB_NAME)
        else:
            print("❌ Input Error: Unrecognized instruction. Please choose options 1-7.")

if __name__ == "__main__":
    main()
