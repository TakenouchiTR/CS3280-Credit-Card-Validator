#!/usr/bin/env python3 
"""
Library file for the first project for CS 3280

Utilities for checking if a credit card number is a valid length, only contains 
digits, and passes the Luhn algorithm.
"""
import re

__author__ = "Shawn Carter"
__version__ = "Fall 2021"
__pylint__ = "v1.8.3"

def luhn_verified(card_number):
    """
    Checks if a card passes the Luhn algorithm.
    Args: card_number - The specified card number to check
    Returns: True if it passes the Luhn algorithm, otherwise false
    """
    nums = list(map(lambda char: int(char), card_number))
    for i in range(0, len(nums) - 1, 2):
        nums[i] = nums[i] * 2 % 9
    
    return sum(nums) % 10 == 0

def is_valid(card_number):
    """
    Checks if a card is the correct length and only contains digits.
    Args: card_number - The specified card number to check
    Returns: True if it is between 13 and 16 digits long, otherwise false
    """
    check_regex = re.compile(r'^\d{13,16}$')
    return check_regex.match(card_number) != None
