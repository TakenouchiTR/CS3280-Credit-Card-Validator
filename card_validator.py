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

def load_file(file_path):
    result = []

    with open(file_path) as file:
        reader = csv.reader(file, delimiter=";")
        entry = []
        for line in reader:
            entry.append(line[0])
            entry.append(line[1].split(","))
            entry.append(line[2].split(","))
        result.append(entry)

    return result

def validate_number(card_number):
    pass

print(create_number_range(0, 9))