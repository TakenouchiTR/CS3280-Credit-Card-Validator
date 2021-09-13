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
    def test_13_digit_number(self):
        """
        Checks if a string with only 13 digits is valid
        """
        number = "1234567890123"
        self.assertTrue(utils.is_valid(number))
    
    def test_19_digit_number(self):
        """
        Checks if a string with only 19 digits is valid
        """
        number = "1234567890123456789"
        self.assertTrue(utils.is_valid(number))

    def test_12_digit_number(self):
        """
        Checks if a string with only 12 digits is invalid
        """
        number = "123456789012"
        self.assertFalse(utils.is_valid(number))
    
    def test_20_digit_number(self):
        """
        Checks if a string with only 20 digits is invalid
        """
        number = "12345678901234567890"
        self.assertFalse(utils.is_valid(number))
    
    def test_16_digit_dash_separated_number(self):
        """
        Checks if a string with 16 digits, separated by dashes into 4 groups of 
        4 digits, is valid
        """
        number = "1234-5678-9012-3456"
        self.assertTrue(utils.is_valid(number))

    def test_16_digit_space_separated_number(self):
        """
        Checks if a string with 16 digits, separated by spaces into 4 groups of 
        4 digits, is valid
        """
        number = "1234 5678 9012 3456"
        self.assertTrue(utils.is_valid(number))
    
    def test_12_digit_space_separated_number(self):
        """
        Checks if a string with 12 digits, separated by dashes into 3 groups of 
        4 digits, is invalid
        """
        number = "1234-5678-9012"
        self.assertFalse(utils.is_valid(number))

    def test_12_digit_space_separated_number(self):
        """
        Checks if a string with 12 digits, separated by spaces into 3 groups of 
        4 digits, is invalid
        """
        number = "1234 5678 9012"
        self.assertFalse(utils.is_valid(number))
    
    def test_20_digit_space_separated_number(self):
        """
        Checks if a string with 12 digits, separated by dashes into 5 groups of 
        4 digits, is invalid
        """
        number = "1234-5678-9012-3456-7890"
        self.assertFalse(utils.is_valid(number))

    def test_20_digit_space_separated_number(self):
        """
        Checks if a string with 12 digits, separated by spaces into 5 groups of 
        4 digits, is invalid
        """
        number = "1234 5678 9012 3456 7890"
        self.assertFalse(utils.is_valid(number))
    
    def test_number_with_digit_characters(self):
        """
        Checks if a string that includes non-digit characters is invalid
        """
        number = "123456789b0123456a"
        self.assertFalse(utils.is_valid(number))


class TestLuhnVerified(unittest.TestCase):
    """
    Tests the luhn_verified() function
    """
    def test_valid_number(self):
        """
        Checks if a valid number is Luhn verified
        """
        number = "345687098585381"
        self.assertTrue(utils.luhn_verified(number))
    
    def test_wrong_check_sum(self):
        """
        Checks if a valid number with an invalid checksum is not Luhn verified
        """
        number = "345687098585380"
        self.assertFalse(utils.luhn_verified(number))
