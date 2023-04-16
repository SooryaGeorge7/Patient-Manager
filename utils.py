"""
This is the file that contains the functions that
are called throughout the application
"""
# Import modules to clear interval, for pattern matching, text colors
# Learnt do make function to clear terminal here:
# https://stackoverflow.com/questions/2084508/clear-terminal-in-python
# Learnt about pattern matching here:
# https://www.geeksforgeeks.org/pattern-matching-python-regex/
# Learnt how to use colorama here:
# https://linuxhint.com/colorama-python/

import os
import re
from colorama import Fore


def not_empty(user_text):
    """
    Function that makes sure that user doesnt enter an empty string
    """
    while True:
        user_input = input(user_text)
        # Use len() to check length of inputted string
        if len(user_input) == 0:
            print(f"{Fore.RED} You've entered an empty string")
        else:
            return user_input


def file_no_pattern(user_text):
    """
    Function that makes sure that user inputs the file number in
    the correct pattern/format
    """
    while True:
        # While loop is used so that user is asked until correct pattern
        user_pattern = input(user_text)
        # Use pattern matching to make sure user enters file in format
        file_pattern = r"^#[0-9]{5}$"
        # re.match() is user to match pattern to user input
        if re.match(file_pattern, user_pattern):
            return user_pattern
        else:
            print(f"{Fore.RED} You have not entered"
                  " file no in the correct format."
                  " Please start with # followed by"
                  " 5 digits eg(#01234)")


def clear_terminal():
    """
    Function that can be called to clear terminal at any stage of the program
    """
    os.system('cls' if os.name == 'nt' else 'clear')
