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
    """Categorizes the Testing for the Functions Modules."""

    def setUp(self) -> None:
    """Sets up the data collections in the system memory prior to the Test Cases."""
    # 1. Gets the Object-Oriented Design Model for validation:
    self.habit_1 = Habit(1, "Drink 2L water", "daily", datetime.now(), datetime.now())
    self.habit_2 = Habit(2, "Go to the gym", "daily", datetime.now(), datetime.now())
    self.habit_3 = Habit(3, "Wash the car", "weekly", datetime.now(), datetime.now())
        
    # 2. Arranges the date collections for tracking habit/task completions.
    self.base_date = datetime(2026, 9, 1, 8, 0)
        
    # Successful 'daily' completion logs for a 4-day "streak":
    self.successful_daily_logs = [
        CompletionLog(101, 1, self.base_date),
        CompletionLog(102, 1, self.base_date + timedelta(days=1)),
        CompletionLog(103, 1, self.base_date + timedelta(days=2)),
        CompletionLog(104, 1, self.base_date + timedelta(days=3))
    ]

    # Gapped 'daily' completion logs for: 3 days completed, 2 days broken, 2 days completed:
    self.gapped_daily_logs = [
        CompletionLog(201, 2, self.base_date),
        CompletionLog(202, 2, self.base_date + timedelta(days=1)),
        CompletionLog(203, 2, self.base_date + timedelta(days=2)),
        # Habit "broken" Constraint:
        CompletionLog(204, 2, self.base_date + timedelta(days=5)),
        CompletionLog(205, 2, self.base_date + timedelta(days=6))
    ] 
    
    # Successful 'weekly' completion logs for a 3-week "streak":
    self.weekly_logs = [
        CompletionLog(301, 3, self.base_date),
        CompletionLog(302, 3, self.base_date + timedelta(weeks=1)),
        CompletionLog(303, 3, self.base_date + timedelta(weeks=2))
    ]

    # Combines categories into a Master Log repository:
    self.master_logs_registry = self.successful_daily_logs + self.gapped_daily_logs + self.weekly_logs

    def test_list_all_habits_cloning(self) -> None:
        """Validation for fetching and listing all habits/tasks without modifying the original data."""
        result = list_all_habits(self.mock_habits_list)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].habit_name, "Drink 2L water")

    def test_filter_by_periodicity_daily(self) -> None:
        """Constraint Validation for grouping records to 'daily' frequency."""
        daily_subset = filter_by_periodicity(self.mock_habits_list, "daily")
        self.assertEqual(len(daily_subset), 2)
        # Ensures chosen intervals pass through filter:
        self.assertTrue(all(h.periodicity == "daily" for h in daily_subset))

    def test_filter_by_periodicity_weekly(self) -> None:
        """Constraint Validation for grouping records to 'weekly' frequency."""
        weekly_subset = filter_by_periodicity(self.mock_habits_list, "weekly")
        self.assertEqual(len(weekly_subset), 1)
        self.assertEqual(weekly_subset[0].habit_name, "Wash the car")

    def test_calculate_successful_daily_streak(self) -> None:
        """Validation for successful 'daily' "streak" returns."""
        raw_dates = [log.completed_at for log in self.perfect_daily_logs]
        streak_result = calculate_streak_for_single_habit(raw_dates, periodicity="daily")
        self.assertEqual(streak_result, 4)

    def test_calculate_gapped_daily_streak_resets_properly(self) -> None:
        """Validation for "broken" habits getting reset - to avoid streaks adding up after habit is "broken"."""
        raw_dates = [log.completed_at for log in self.gapped_daily_logs]
        streak_result = calculate_streak_for_single_habit(raw_dates, periodicity="daily")
        # Equation detects 3-day "streak" as the historical maximum, and reset the current "streak":
        self.assertEqual(streak_result, 3)

    def test_get_longest_streak_for_single_habit(self) -> None:
        """Validation for a single habit "streak" - filtering the longest one specifically."""
        # Habit 2 had been "broken":
        max_streak_gym = get_longest_streak_one(2, self.master_logs_registry, "daily")
        self.assertEqual(max_streak_gym, 3)
        
    def test_get_longest_streak_across_entire_system(self) -> None:
        """Validation for the maximum "streak" for ALL habits"""
        absolute_top_streak = get_longest_streak_all(self.mock_habits_list, self.master_logs_registry)
        # Habit 1 which had the longest "streak":
        self.assertEqual(absolute_top_streak, 4)

if __name__ == '__main__':
    unittest.main()
