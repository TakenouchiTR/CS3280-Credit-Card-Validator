import unittest
import re
import card_validator

class TestCreateNumberRange(unittest.TestCase):
    def test_single_digit_numbers(self):
        number_one = 0
        number_two = 8

        regex_string = card_validator.create_number_range(number_one, number_two)
        regex = re.compile(regex_string)

        for i in range(number_one, number_two + 1):
            self.assertTrue(regex.match(str(i)))

    def test_five_digit_numbers(self):
        number_one = 12345
        number_two = 23456

        regex_string = card_validator.create_number_range(number_one, number_two)
        regex = re.compile(regex_string)

        for i in range(number_one, number_two + 1):
            self.assertTrue(regex.match(str(i)))
    
    def test_first_number_larger_than_second(self):
        number_one = 98765
        number_two = 23456

        regex_string = card_validator.create_number_range(number_one, number_two)
        regex = re.compile(regex_string)

        for i in range(number_one, number_two + 1):
            self.assertTrue(regex.match(str(i)))

    def test_numbers_are_different_lengths(self):
        number_one = 5
        number_two = 1234
        size_difference = 3

        regex_string = card_validator.create_number_range(number_one, number_two)
        regex = re.compile(regex_string)

        for i in range(number_one, number_two + 1):
            num = str(i)
            num = ("0" * (size_difference - len(num) + 1)) + num
            self.assertTrue(regex.match(num))
    
    def test_second_number_ends_in_zero(self):
        number_one = 10000
        number_two = 15000

        regex_string = card_validator.create_number_range(number_one, number_two)
        regex = re.compile(regex_string)

        for i in range(number_one, number_two + 1):
            self.assertTrue(regex.match(str(i)))