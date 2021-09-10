import csv
import re

def create_number_range(min, max):
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

def parse_starting_digits(data):
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
        
def get_number_length(data, starting_digit_length):
    result = ""
    data_sections = data.split(",")

    for i in range(len(data_sections)):
        length = int(data_sections[i])
        if i == 0:
            result += r"\d"
            result += "{{{}}}".format(length - starting_digit_length)
        else:
            result += r"(\d"
            prev_length = int(data_sections[i - 1])
            result += "{{{}}})?".format(length - prev_length)

    return result

def load_file(file_path):
    result = []

    with open(file_path) as file:
        reader = csv.reader(file, delimiter=";")
        for issuer, card_lengths, starting_digits in reader:
            start_digit_regexes = parse_starting_digits(starting_digits)
            for key in start_digit_regexes:
                regex_string = "^"
                regex_string += "({})".format(start_digit_regexes[key])
                regex_string += get_number_length(card_lengths, key)
                regex_string += "$"
                result.append((regex_string, issuer))

    return result

def luhn_verified(card_number):
    nums = list(map(lambda char: int(char), card_number))
    for i in range(0, len(nums) - 1, 2):
        nums[i] = nums[i] * 2 % 9
    
    return sum(nums) % 10 == 0

def display_card_information(card_number, card_type):
    authenticity = "N/A"

    if card_type == "Invalid":
        card_number = "Invalid"
    elif luhn_verified(card_number):
        authenticity = "Authentic."
    else:
        authenticity = "Fake."

    print("Credit card number: {}".format(card_number))
    print("Credit card type:   {}".format(card_type))
    print("Luhn verification:  {}".format(authenticity))

def format_separated_number(card_number):
    number_separation_regexes = [
        re.compile(r"^(\d{4})-(\d{4})-(\d{4})-(\d{4})$"),
        re.compile(r"^(\d{4}) (\d{4}) (\d{4}) (\d{4})$")
    ]
    
    for separation_regex in number_separation_regexes:
        if separation_regex.match(card_number):
            card_sections = separation_regex.findall(card_number)
            return "".join(card_sections[0])
    
    return card_number

def validate_number(card_number):
    db = load_file("C:\\Users\\Shawn\\Documents\\School\\CS 3280 Sys Prog\\Project 1\\credit_card_types.ssv")
    card_type = "Invalid"

    card_number = format_separated_number(card_number)

    for regex_string, issuer in db:
        card_regex = re.compile(regex_string)
        if card_regex.match(card_number):
            card_type = issuer
            break
    
    display_card_information(card_number, card_type)


validate_number("5275 1900 0427 8764")