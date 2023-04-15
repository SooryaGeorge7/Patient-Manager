"""
This is the main file that runs the patient manager application
"""
# import re
# import datetime
# import getpass
# import gspread
# from google.oauth2.service_account import Credentials
# from colorama import Fore, Style
# import bcrypt
# from google_sheets_api import patients, appointments, treatments
# from utils import clear_terminal, file_no_pattern
from startup_options import logo, choice
# from main_menu import menu_choice


# SCOPE = [
#    "https://www.googleapis.com/auth/spreadsheets",
#    "https://www.googleapis.com/auth/drive.file",
#    "https://www.googleapis.com/auth/drive"
#    ]

# CREDS = Credentials.from_service_account_file('creds.json')
# SCOPED_CREDS = CREDS.with_scopes(SCOPE)
# GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
# SHEET = GSPREAD_CLIENT.open('Patient_manager')
# users = SHEET.worksheet('users')
# patients = SHEET.worksheet('patients')
# appointments = SHEET.worksheet('appointments')
# treatments = SHEET.worksheet('treatments')
# treatments_data = treatments.get_all_values()

# Learnt how to use colorama here
# https://www.geeksforgeeks.org/pattern-matching-python-regex/


def main():
    """
    This main function calls the logo function and
    choice function to start the program
    """
    logo()
    choice()


main()
