"""
This is the file that contains google sheet API connections
"""
# Import data from google sheets
import gspread
from google.oauth2.service_account import Credentials


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# Creds.json is added to gitignore
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Patient_manager')

# The sheets from google sheets that are used by app
users = SHEET.worksheet('users')
patients = SHEET.worksheet('patients')
appointments = SHEET.worksheet('appointments')
treatments = SHEET.worksheet('treatments')
