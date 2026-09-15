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
    """ Sets up the data collections in the system memory prior to the Test Cases.
    # 1. Gets the Object-Oriented Design Model for validation:
    self.habit_1 = Habit(1, "Drink 2L water", "daily", datetime.now(), datetime.now())
    self.habit_2 = Habit(2, "Go to the gym", "weekly", datetime.now(), datetime.now())
    self.habit_3 = Habit(3, "Wash the Car", "weekly", datetime.now(), datetime.now())
        














