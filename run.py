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

patients = SHEET.worksheet('patients')

patient_data = patients.get_all_values()

def sign_up():
    sign_in = False
    while sign_in == False:
        new_username = input("Please enter a new username:")
        new_row = []
        for line in data:
            if new_username == line[0]:
                print("The username is already taken, please try again.")
                #allow user to enter username again  if its already been used.
                new_username = input("Please enter a new username:")
                #ask user for the neewpassword , and confirm password using input()             
        new_password = input("Please enter a new password:")
        confirm_password = input("Please reenter password to confirm:")
    
        if confirm_password != new_password:
            print("Passwords dont match, please try again!")
            pass
        else:
            sign_in = True
            print("Sign Up Succesfull")
            new_row.append(new_username)
            new_row.append(new_password)
            print(new_row)
            users.append_row(new_row)
            break

class Patient:
    def __init__(self,file_number):
        self.file_number = file_number
        self.details = self.patient_details(file_number)
    
    def patient_details(self,file_number):
        file_number_column = patients.col_values(5)
        row = file_number_column.index(file_number) + 1

        details = patients.row_values(row)

        return details


user_choice = input("Please choose from options below:(type in a or b)\n a) Log in \n b) Register \n Choice: ")

if user_choice == "a":
    log_in = False
elif user_choice == "b":
    sign_up()
    log_in = False
else:
    user_choice = input("Please choose from options below:(type in a or b)\n a) Log in \n b) Register \n Choice: ")
      
while log_in == False:
    print("You may log in!")
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


while log_in == True:
    menu = input('''\n Please select one of the following Options below:\n
a - View patient details
b - Add new patient
c - Add appointment
d - View Treatment Costs
e - Exit
: ''').lower()
    if menu == "a":
        file_number = input("Enter patient's file number: ")
        patient = Patient(file_number)
        print("Patient details are as follows")
        print(f''' Patient Name:{patient.details[0]}\n Patient Surname:{patient.details[1]}\n Email:{patient.details[2]}\n Birthday:{patient.details[3]}\n File Number:{patient.details[4]}''')
    elif menu == "b":
        add_patient()
    
    elif menu == "c":
        add_appointment()

    elif menu == "d":
        view_treatments()

    elif menu == "e":
        print("Goodbye")    
        exit()

    else:
        print("You have entered an invalid option, Please try again")

