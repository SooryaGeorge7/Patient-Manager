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
                  " 5 digits eg(#12345)")


def clear_terminal():
    """
    Function that can be called to clear terminal at any stage of the program
    """
    # Learnt here
    # https://stackoverflow.com/questions/4810537/how-to-clear-the-screen-in-python
    os.system('cls' if os.name == 'nt' else 'clear')
