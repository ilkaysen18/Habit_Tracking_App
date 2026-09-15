"""
"ANALYTICS MODULE" CLASS:

Functional Promramming Analytics Suite Module:
This Library utilizes functions for habits and logs, by handling the following:
- data transformations,
- subsetting pipelines,
- mathematical evaluations.
"""


from datetime import datetime, timedelta


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
    ....
    Args:
        logs (list):
    Returns:
        int:
    """
    




