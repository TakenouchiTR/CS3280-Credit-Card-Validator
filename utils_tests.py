#!/usr/bin/env python3
"""
Tests for the utils.py lirary
"""
import unittest
import utils

__author__ = "Shawn Carter"
__version__ = "Fall 2021"
__pylint__ = "v1.8.3"

class TestIsValid(unittest.TestCase):
    """
    Tests for the is_valid() function
    """
    def test_16_digit_number(self):
        """
        Checks if a string with only 16 digits is valid
        """
        number = "1234567890123456"
        self.assertTrue(utils.is_valid(number))

class TestLuhnVerified(unittest.TestCase):
    """
    Tests the luhn_verified() function
    """
    def test_valid_number(self):
        """
        Checks if a valid valid number is counted as valid
        """
        number = "345687098585381"
        self.assertTrue(utils.luhn_verified(number))
