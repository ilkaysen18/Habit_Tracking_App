"""
"ANALYTICS MODULE" CLASS:

Functional Promramming Analytics Suite Module:
This Library utilizes functions for habits and logs, by handling the following:
- data transformations,
- subsetting pipelines,
- mathematical evaluations.
"""



from datetime import datetime, timedelta



"""FUNCTIONS LISTED BELOW:"""


def list_all_habits(habits: list) -> list:
    """
    Lists all currently tracked habits/tasks.
    Args:
        habits (list): This is a list that contains the the Habit Attribute's database Objects.
    Returns:
        list: An array that contains all tracked Classes/Entities.
    """
    return [habit for habit in habits]


def filter_by_periodicity(habits: list, periodicity: str) -> list:
    """
    This subsets specific Habit collections - in this case, filtering by periodicity. 
    Args:
        habits (list): A list of current Habit records in the system.
        periodicity (str): The target Time Delta, filtering by frequency (e.g. 'daily', 'weekly', etc.).
    Returns:
        list: A filtered subset of habits that match the Threshold Bounds.
    """
    return [h for h in habits if h.periodicity.lower() == periodicity.lower()]


def calculate_streak_for_single_habit(logs: list, periodicity: str) -> int:
    """
    Computes the longest consecutive sequence for habit/task completion.
    Args:
        logs (list): Lists datetime for successful completion logs.
        periodicity (str): Frequency Constraint.
    Returns:
        int: The highest calculated number of uninterrupted habit/task completions.
    """
    if not logs:
        return 0

    # 1. Clean Data Pipeline - Extracts specific sorted dates:
    sorted_dates = sorted(list(set([dt.date() for dt in logs])))

    # Defines the maximum gap Delta Time bounds based on the periodicity:
    if periodicity.lower() == "daily":
        max_gap = timedelta(days=1)
    elif periodicity.lower() == "biweekly":
        max_gap = timedelta(days=3)
    elif periodicity.lower() == "weekly":
        max_gap = timedelta(weeks=1)
    else:
        max_gap = timedelta(days=14)

    # 2. Recursive connection (Loops) to other Constraints:
    def accumulate_streaks(dates_list, current_streak, max_streak):
        if len(dates_list) <= 1:
            return max(max_streak, current_streak)
        
        # Measures chronological distance between neighboring habit/task completions:
        gap = dates_list[1] - dates_list[0]

        if gap <= max_gap:
            # If the habit/task completion "streak" is held:
            return accumulate_streaks(dates_list[1:], new_current, max(max_streak, new_current))
        elif gap > max_gap:
            #If the habit/task completion "streak" is broken:
            return accumulate_streaks(dates_list[1:], 1, max_streak)
    
    # Returns the defined function:
    return accumulate_streaks(sorted_dates, 1, 1)


def get_longest_streak_one(habit_id: int, all_logs: list, periodicity: str) -> int:
    """
    Computes the maximum historic completion streak achieved by user, for a specific habit.
    Args:
       habit_id (int): FK - Relational Foreign Key that connects matching target habit fields.
       all_logs (list): The unfiltered list of all completion logs.
       periodicity (str): Frequency.
    Returns:
        int: The longest "streak" of habit/task completion for the specific habit.
    """

    # Functional Filter Pipeline: This extracts the relevant Child Logs that match the Parent ID strings:
    target_timestamps = [log.completed_at for log in all_logs if log.habit_id == habit_id]
    return calculate_streak_for_single_habit(target_timestamps, periodicity)


def get_longest_streak_all(habits: list, all_logs: list):
    """Finds the longest 'streak' from ALL habit completion logs.

    Returns:
        tuple: (best_habit, best_streak)
    """
    if not habits:
        return None, 0

    best_habit = None
    best_streak = 0

    for h in habits:
        s = get_longest_streak_one(h.habit_id, all_logs, h.periodicity)

        # if your get_longest_streak_one returns None sometimes, guard it:
        if s is None:
            continue

        if s > best_streak:
            best_streak = s
            best_habit = h

    return best_habit, best_streak
