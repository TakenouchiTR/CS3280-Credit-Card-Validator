#!/usr/bin/env python3 
import re

__author__ = "Shawn Carter"
__version__ = "Fall 2021"
__pylint__ = "v1.8.3"

def luhn_verified(card_number):
    nums = list(map(lambda char: int(char), card_number))
    for i in range(0, len(nums) - 1, 2):
        nums[i] = nums[i] * 2 % 9
    
    return sum(nums) % 10 == 0

def is_valid(card_number):
    check_regex = re.compile(r'^\d{13,16}$')
    return check_regex.match(card_number) != None
