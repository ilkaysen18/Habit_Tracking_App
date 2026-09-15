"""
AUTOMATED UNIT TESTING VALIDATION SUITE:

This Module holds the Testing information to test the
(mathematical) validity of the "Analytics Module".
"""


import unittest 
from datetime import datetime, timedelta
from models.habit import Habit
from models.completion_log import CompletionLog
from modules.analytics import (
    list_all_habits,
    filter_by_periodicity,
    calculate_streak_for_single_habit,
    get_longest_streak_one,
    get_longest_streak_all
)


class TestHabitTrackerAnalytics(unittest.TestCase):
    """ Categorizes the Testing for the Functions Modules. """

    def setUp(self) -> None:
    """ Sets up the data collections in the system memory prior to the Test Cases. """
    # 1. Gets the Object-Oriented Design Model for validation:
    self.habit_1 = Habit(1, "Drink 2L water", "daily", datetime.now(), datetime.now())
    self.habit_2 = Habit(2, "Go to the gym", "weekly", datetime.now(), datetime.now())
    self.habit_3 = Habit(3, "Go out with friends", "biweekly", datetime.now(), datetime.now())
        
    # 2. Arranges the date collections for tracking habit/task completions.
    self.base_date = datetime(2026, 9, 1, 8, 0)
    
    # Successful 'daily' completion logs for a 4-day "streak":
    self.successful_daily_logs = [
        CompletionLog(101, 1, self.base_date),
        CompletionLog(102, 1, self.base_date + timedelta(days=1)),
        CompletionLog(103, 1, self.base_date + timedelta(days=2)),
        CompletionLog(104, 1, self.base_date + timedelta(days=3))
    ]

    # Gapped 'biweekly' completion logs for a 2 weeks completed and a 2 weeks broken:
    self.gapped_daily_logs = [
        CompletionLog(201, 2, self.base_date),
        CompletionLog(202, 2, self.base_date + timedelta(weeks=1)),
        CompletionLog(203, 2, self.base_date + timedelta(weeks=2)),
        # Habit "broken" Constraint:
        CompletionLog(204, 2, self.base_date + timedelta(weeks=5)),
        CompletionLog(205, 2, self.base_date + timedelta(days=6))
    ]

    # Successful 'fortnightly' completion logs for a 2-fortnightly "streak":
    self.weekly_logs = [
        CompletionLog(301, 2, self.base_date),
        CompletionLog(302, 2, self.base_date + timedelta(fortnights=1)),
        CompletionLog(303, 3, self.base_date + timedelta(fortnights=2))
    ]

    # Combines categories into a Master Log repository:
    self.master_logs_registry = self.successful_daily_logs + self.gapped_daily_logs + self.weekly_logs

    def test_list_all_habits_cloning(self) -> None:










