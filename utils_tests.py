import unittest
import re
import utils

class TestCreateNumberRange(unittest.TestCase):
    def test_single_digit_numbers(self):
        number_one = 0
        number_two = 8

        regex_string = utils.create_number_range(number_one, number_two)
        regex = re.compile(regex_string)

        for i in range(number_one, number_two + 1):
            self.assertTrue(regex.match(str(i)))

    def test_five_digit_numbers(self):
        number_one = 12345
        number_two = 23456

        regex_string = utils.create_number_range(number_one, number_two)
        regex = re.compile(regex_string)

        for i in range(number_one, number_two + 1):
            self.assertTrue(regex.match(str(i)))
    
    def test_first_number_larger_than_second(self):
        number_one = 98765
        number_two = 23456

        regex_string = utils.create_number_range(number_one, number_two)
        regex = re.compile(regex_string)

        for i in range(number_one, number_two + 1):
            self.assertTrue(regex.match(str(i)))

    def test_numbers_are_different_lengths(self):
        number_one = 5
        number_two = 1234
        size_difference = 3

        regex_string = utils.create_number_range(number_one, number_two)
        regex = re.compile(regex_string)

        for i in range(number_one, number_two + 1):
            num = str(i)
            num = ("0" * (size_difference - len(num) + 1)) + num
            self.assertTrue(regex.match(num))
    
    def test_second_number_ends_in_zero(self):
        number_one = 10000
        number_two = 15000

        regex_string = utils.create_number_range(number_one, number_two)
        regex = re.compile(regex_string)

        for i in range(number_one, number_two + 1):
            self.assertTrue(regex.match(str(i)))

class TestParseStartingDigits(unittest.TestCase):
    def test_single_number(self):
        num_string = "32"
        regex_string = utils.parse_starting_digits(num_string)
        self.assertEqual(regex_string, {2: "32"})
    
    def test_two_numbers(self):
        num_string = "32,35"
        regex_string = utils.parse_starting_digits(num_string)
        self.assertEqual(regex_string, {2: "32|35"})
    
    def test_number_range_no_similar_digits(self):
        num_string = "1003-2375"
        regex_string = utils.parse_starting_digits(num_string)
        self.assertEqual(regex_string, {4: "(100[3-9]|10[1-9][0-9]{1}|1[1-9][0-9]{2}|2[0-2][0-9]{2}|23[0-6][0-9]{1}|237[0-5])"})
    
    def test_number_range_with_similar_digits(self):
        num_string = "1003-1075"
        regex_string = utils.parse_starting_digits(num_string)
        self.assertEqual(regex_string, {4: "(10(0[3-9]|[1-6][0-9]{1}|7[0-5]))"})

    def test_number_range_and_single_numbers(self):
        num_string = "1003-1075,35,36"
        regex_string = utils.parse_starting_digits(num_string)
        self.assertEqual(regex_string, {4: "(10(0[3-9]|[1-6][0-9]{1}|7[0-5]))", 2: "35|36"})

class TestGetNumberLength(unittest.TestCase):
    def test_single_number(self):
        num_string = "16"
        starting_digit_length = 5
        regex_string = utils.get_number_length(num_string, starting_digit_length)
        self.assertEqual(regex_string, r"\d{11}")
    
    def test_two_numbers(self):
        num_string = "16,19"
        starting_digit_length = 5
        regex_string = utils.get_number_length(num_string, starting_digit_length)
        self.assertEqual(regex_string, r"\d{11}(\d{3})?")