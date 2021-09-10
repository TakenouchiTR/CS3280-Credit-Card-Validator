#!/usr/bin/env python3
import unittest
import utils

__author__ = "Shawn Carter"
__version__ = "Fall 2021"
__pylint__ = "v1.8.3"

class TestIsValid(unittest.TestCase):
    def test_16_digit_number(self):
        number = "1234567890123456"
        self.assertTrue(utils.is_valid(number))

class TestLuhnVerified(unittest.TestCase):
    def test_valid_number(self):
        number = "345687098585381"
        self.assertTrue(utils.luhn_verified(number))
