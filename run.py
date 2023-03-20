# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
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

data = users.get_all_values()

user_choice = input("Please choose from options below:(type in a or b)\n a) Log in \n b) Register \n Choice: ")

if user_choice == "a":
    log_in = False
elif user_choice == "b":
    sign_up()
else:
    user_choice = input("Please choose from options below:(type in a or b)\n a) Log in \n b) Register \n Choice: ")
      
while log_in == False:
    login_username = input("Please enter username: ")
    login_password = input("Please enter password: ")
    for line in data:
        correct_username = line[0]
        correct_password = line[1]
        if login_username == correct_username and login_password == correct_password :
            log_in = True
            print("Log in Successful!")
        elif login_username != correct_username and login_password == correct_password :
            print("You've entered an invalid username try again")
            pass
        elif login_username == correct_username and login_password != correct_password :
            print("Your password is incorrect, try again")
            pass
        elif login_username == correct_username and login_password != correct_password :
            print("Both your username and password is incorrect" )
            pass


