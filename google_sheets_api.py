"""
This is the file that contains google sheet API connections
"""

import gspread
from google.oauth2.service_account import Credentials


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Patient_manager')
users = SHEET.worksheet('users')
patients = SHEET.worksheet('patients')
appointments = SHEET.worksheet('appointments')
treatments = SHEET.worksheet('treatments')
treatments_data = treatments.get_all_values()