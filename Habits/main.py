"""
HABIT TRACKER CLI CLASS - MAIN GATEWAY FOR COMMAND LINE INTERFACE LAYER:

This Module holds the Menu loop and validates user input flows.
It connects the Database to the Analytics.
"""



import sys
from datetime import datetime
from database.db_manager import initialize_tables, seed_predefined_fixtures, get_connection
from models.habit import Habit
from models.completion_log import CompletionLog
from modules.analytics import (
    list_all_habits,
    filter_by_periodicity,
    get_longest_streak_one,
    get_longest_streak_all
)



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

    for idx, h in enumerate(habits):
completed_habits = completion_logs(habit_id, completed_at)
print(f"{idx + 1}. {h.habit_name} [{h.periodicity}]")
not completed_habits(habit_id, completed_at)

    try:
        selection = int(input("\nSelect habit index row to complete: ")) - 1
        if selection < 0 or selection >= len(habits):
            raise IndexError

        target_habit = habits[selection]
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

    if periodicity.lower() == "daily":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)

    elif periodicity.lower() == "weekly":
        # week window: from Monday 00:00 to next Monday 00:00
        start = now - timedelta(days=now.weekday())
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(weeks=1)

    else:
        # Fallback: treat as "not completed" unless you implement the window
        return False

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







def run_analytics_dashboard(habits: list, logs: list) -> None:
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
            # Expands array to match periodicity bounds:
            valid_filters = ["daily", "weekly", "biweekly", "fortnightly", "monthly", "yearly"]
            
            print("\nAvailable filters: " + ", ".join(valid_filters))
            p = input("Enter frequency: ").strip().lower()
            
            if p in valid_filters:
                filtered = filter_by_periodicity(habits, p)
                print(f"\n🔍 ONLY SHOWING {p.upper()} TRACKERS:")
                if not filtered:
                    print("  No habits found matching this timeframe.")
                for h in filtered:
                    print(f" • {h.habit_name}")
            else:
                print("❌ Invalid filter bounds entered.")
                
        elif choice == "3":
            top_run = get_longest_streak_all(habits, logs)
            print(f"\n🏆 Absolute Longest System-Wide Streak: {top_run} consecutive periods!")
            
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
		print("4. Terminate State Machine & Exit")

		choice = input("\nSelect option coordinate (1-4): ").strip()

		if choice == "1":
			create_new_habit_flow(habits)
		elif choice == "2":
			check_off_habit_flow(habits)
		elif choice == "3":
			run_analytics_dashboard(habits, logs)
		elif choice == "4":
			print("\nProgress securely saved to local storage file. Closing runtime loop. Goodbye!")
			sys.exit()
		else:
			print("❌ Input Error: Unrecognized instruction. Please choose options 1-4.")

if __name__ == "__main__":
	main()
