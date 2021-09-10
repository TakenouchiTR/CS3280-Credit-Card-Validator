#!/usr/bin/env python3
"""
The first project for CS 3280

This script accepts a credit card number from the user, then displays
who issued the card and whether or not the card number is valid.
"""
import sys
import re
import csv
import utils

__author__ = "Shawn Carter"
__version__ = "Fall 2021"
__pylint__ = "v1.8.3"

INVALID = "Invalid"

def format_separated_number(card_number):
    """
    Checks if the card number is a 16-digit long number separated by spaces or hyphens.
    If the number is made of four groups of four digits, the separators are removed.
    Args: card_number - The specified card number
    Returns: card_number without the separators if it matches the specified pattern, otherwise
             card_number is returned unaltered
    """
    number_separation_regexes = [
        re.compile(r"^(\d{4})-(\d{4})-(\d{4})-(\d{4})$"),
        re.compile(r"^(\d{4}) (\d{4}) (\d{4}) (\d{4})$")
    ]
    
    for separation_regex in number_separation_regexes:
        if separation_regex.match(card_number):
            card_sections = separation_regex.findall(card_number)
            return "".join(card_sections[0])
    
    return card_number

def get_card_number():
    """
    Prompts the user for a card number. If a third argument exists, it will be returned 
    as the card number itself.
    Args: None
    Returns: The user-specified card number
    """
    card_number = ""
    if len(sys.argv) == 3:
        card_number = sys.argv[2]
    else:
        card_number = input("Please enter a credit card number:\n")
    
    card_number = format_separated_number(card_number)
    return card_number

def create_number_range(min, max):
    """
    Accepts a minimum and maximum value and creates a string for a regular expression that 
    checks for any number across the range.
    Args: min - The minimum value, inclusive
          max - the maximum value, inclusive
    Returns: An uncompiled regular expression string
    """
    result = ""

    if min > max:
        min, max = max, min
    
    max_str = str(max)
    min_str = str(min)

    min_str = ("0" * (len(max_str) - len(min_str))) + min_str

    prefix_len = 0
    while min_str[prefix_len] == max_str[prefix_len]:
        prefix_len += 1
    
    if prefix_len > 0:
        result += min_str[:prefix_len]
        result += "("

    for i in reversed(range(prefix_len, len(min_str))):
        num_search = ""
        if i == len(min_str) - 1:
            num_search += min_str[prefix_len:i]
            num_search += "[{}-9]".format(min_str[i])
        elif i != prefix_len:
            num_search += "|{}".format(min_str[prefix_len:i])
            num_search += "[{}-9]".format(int(min_str[i]) + 1)
            num_search += "[0-9]{{{}}}".format(len(min_str) - i - 1)
        elif int(min_str[i]) < int(max_str[i]) - 1:
            num_search += "|[{}-{}]".format(int(min_str[i]) + 1, int(max_str[i]) - 1)
            num_search += "[0-9]{{{}}}".format(len(min_str) - i - 1)
        result += num_search
    
    for i in range(prefix_len + 1, len(max_str)):
        num_search = "|"
        if i == len(max_str) - 1:
            if max_str[i] == '0':
                num_search += max_str[prefix_len:]
            else:
                num_search += max_str[prefix_len:i]
                num_search += "[0-{}]".format(int(max_str[i]))
            result += num_search
        elif max_str[i] != "0":
            num_search += max_str[prefix_len:i]
            num_search += "[0-{}]".format(int(max_str[i]) - 1)
            num_search += "[0-9]{{{}}}".format(len(max_str) - i - 1)
            result += num_search

    if prefix_len > 0:
        result += ")"

    return result

def parse_prefixes(data):
    """
    Accepts a string of comma-separated values and parses it into an uncompiled 
    regular expression string.
    Ranges can be set by having two numbers separated by a hyphen
    Args: data - The string of comma-separated values
    Returns: An uncompiled regular expression string for checking all prefixes
    """
    result = {}

    for data_item in data.split(","):
        if "-" in data_item:
            data_range = data_item.split("-")
            starting_digit_length = max(len(data_range[0]), len(data_range[1]))

            if starting_digit_length not in result:
                result[starting_digit_length] = "("
            else:
                result[starting_digit_length] += "|("
            
            result[starting_digit_length] += create_number_range(data_range[0], data_range[1])
            result[starting_digit_length] += ")"
        else:
            starting_digit_length = len(data_item)

            if starting_digit_length not in result:
                result[starting_digit_length] = ""
            else:
                result[starting_digit_length] += "|"
            
            result[starting_digit_length] += str(data_item)
    
    return result
        
def get_number_length(data, prefix_length):
    """
    Creates an uncompiled regular expression string for checking if the correct amount
    of digits exist after the prefix.
    Args: data - The string of comma-separated values representing the valid card lengths
    Returns: An uncompiled regular expression string for checking valid card lengths
    """
    result = ""
    data_sections = data.split(",")

    for i in range(len(data_sections)):
        length = int(data_sections[i])
        if i == 0:
            result += r"\d"
            result += "{{{}}}".format(length - prefix_length)
        else:
            result += r"(\d"
            prev_length = int(data_sections[i - 1])
            result += "{{{}}})?".format(length - prev_length)

    return result

def load_file(file_path):
    """
    Loads a semicolon-separed value file of credit card information and turns it into a list of valuue-pairs.
    The first value is an uncompiled regular expression.
    The second value is the issuer associated with the regular expression.
    Args: file_path - The path to the semicolon-separated value file
    Returns: A list of value-pairs representing card issuers and an uncompiled regular expression for 
             their valid numbers
    """
    result = []

    with open(file_path) as file:
        reader = csv.reader(file, delimiter=";")
        for issuer, card_lengths, starting_digits in reader:
            start_digit_regexes = parse_prefixes(starting_digits)
            for key in start_digit_regexes:
                regex_string = "^"
                regex_string += "({})".format(start_digit_regexes[key])
                regex_string += get_number_length(card_lengths, key)
                regex_string += "$"
                result.append((regex_string, issuer))

    return result

def display_card_information(card_number, issuer):
    """
    Displays information about a credit card, including the card number, issuer, and
    whether it passes the Luhn algorithm. If issuer == INVALID, then the card number
    will be displayed as INVALID and it will not be checked for authenticity.
    Args: card_number - The card number
          issuer - The issuuer for the card
    Returns: None
    """
    authenticity = "N/A"

    if issuer == INVALID:
        card_number = INVALID
    elif utils.luhn_verified(card_number):
        authenticity = "Authentic."
    else:
        authenticity = "Fake."

    print("Credit card number: {}".format(card_number))
    print("Credit card type:   {}".format(issuer))
    print("Luhn verification:  {}".format(authenticity))

def get_card_issuer(card_number, issuer_db):
    """
    Compares a card number against a list of regular expressions. If the
    number matches a regular expression, it will return the issuer associated 
    with it. If there are no matches, INVALID will be returned.
    Args: card_number - The card number to check
          issuer_db - The value-pairs representing issuers and their associated
                      regular expressions
    Returns: The name of the card issuer if a match is found, otherwise INVALID
    """
    for regex_string, issuer in issuer_db:
        card_regex = re.compile(regex_string)
        if card_regex.match(card_number):
            return issuer
    
    return INVALID

def main():
    """
    The main entry point for the script.
    Args: None
    Returns: None
    """
    file_path = ""
    card_number = ""
    issuer = INVALID

    if len(sys.argv) == 1:
        print("Missing data file path")
        exit()
    
    file_path = sys.argv[1]
    card_number = get_card_number()

    if utils.is_valid(card_number):
        issuer_db = load_file(file_path)
        issuer = get_card_issuer(card_number, issuer_db)

    display_card_information(card_number, issuer)

if __name__ == "__main__":
    main()