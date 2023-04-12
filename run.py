"""
Importing libraries and data from libraries and gspread
"""
import re
import os
import datetime
import getpass
import gspread
from google.oauth2.service_account import Credentials
from colorama import Fore, Style
import bcrypt


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

# Learnt how to use colorama here
# https://www.geeksforgeeks.org/pattern-matching-python-regex/


def logo():
    """
    Function that shows the program's logo and gives
    a brief welcome message that allows user to understand
    what the program is about.
    """
    print(f"""{Fore.CYAN}
                _______         _    _                  _
               |_   __ \\       / |_ (_)                / |_
                 | |__) |,--. `| |-'__  .---.  _ .--. `| |-'
                 |  ___/`'_\\ : | | [  |/ /__\\ [ `.-. | | |
                _| |_   // | |,| |, | || \\__., | | | | | |,
               |_____|  \\'-;__/\\__/[___]'.__.'[___||__]\\__/
          ____    ____
         |_   \\  /   _|
           |   \\/   |   ,--.   _ .--.   ,--.   .--./) .---.  _ .--.
           | |\\  /| |  `'_\\ : [ `.-. | `'_\\ : / /'`\\;/ /__\\[ `/'`\\]
          _| |_\\/_| |_ // | |, | | | | // | |,\\ \\._//| \\__., | |
         |_____||_____|\\'-;__/[___||__]\\'-;__/.',__`  '.__.'[___]
                                             ( ( __))
    """)
    print(f"""{Fore.LIGHTWHITE_EX}
                        Welcome to Patient Manager.
           The system to manage patients in your Dental practice.
    {Style.RESET_ALL}""")


def choice():
    """
    Function that allows user to choose between loging in
    or signing in.
    """
    option = False
    while option is False:
        user_choice = input(f"""{Fore.LIGHTYELLOW_EX}
 Please choose from options below(Please register if you havent before):
 a - Log in
 b - Register
 Choice:\n {Style.RESET_ALL}""")
        clear_terminal()
        if user_choice == "a":
            option = True
            # Calls fxn to log in
            user_login()
        elif user_choice == "b":
            # Calls fxn to sign up/register
            sign_up()
            option = True

        else:
            print(f"{Fore.RED} Invalid option, try again{Style.RESET_ALL}")


def user_login():
    """
    Function that allows user to enter username and password
    and validates them by checking with the usernames and passwords stored
    users data sheet. The inputed password has to encoded to check with
    the hashed passwords in data sheet.(You have to encode the passwords
    in datasheet because they were decoded when being stored.)
    """
    # Get values from users SHEET in google sheets using get_all_values().
    data = users.get_all_values()
    log_in = False
    print(f"{Fore.GREEN} You may log in!{Style.RESET_ALL}")
    while log_in is False:
        login_username = input(f"{Fore.LIGHTYELLOW_EX} Please "
                               f"enter username:\n{Style.RESET_ALL} ")
        login_password = getpass.getpass(f"{Fore.LIGHTYELLOW_EX} Please "
                                         f"enter password:"
                                         f"\n{Style.RESET_ALL} ")
        # Encode user input to be able to match hashed one in database.
        coded_password = login_password.encode('utf-8')
        # Call fxn to clear terminal
        clear_terminal()
        try:
            # Use for loop to check for stored usernames and passwords
            for value in data:
                username = value[0]
                password = value[1]
                # Encode the (decoded) string password to change it to bytes
                hash_password = password.encode('utf-8')
                # Use bcrypt.checkpw to check if input matches stored password
                if login_username == username and \
                   bcrypt.checkpw(coded_password, hash_password):
                    print(f"{Fore.GREEN} Log in Successful!{Style.RESET_ALL}")
                    # Call menu fxn
                    menu_choice()
                    break

            else:
                user_option = input(f"""{Fore.RED}
 We dont have those credentials,
 Please choose between":
 {Fore.LIGHTYELLOW_EX}
 a - Try Log in again
 b - Register
 :\n{Style.RESET_ALL} """)
                if user_option == "a":
                    clear_terminal()
                    raise ValueError
                elif user_option == "b":
                    clear_terminal()
                    # Call function to sign in
                    sign_up()
                    break
                else:
                    print(f"{Fore.RED} Invalid option."
                          f"Start again{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED} Please try again{Style.RESET_ALL}")


def sign_up():
    """
    Function that allows user to sign in when user chooses to.
    It allows user to input username and password.
    Checks that the username is not taken already and allows
    username to confirm password and displays error message if user
    gives in an invalid username or if passwords dont match.
    """
    # Gets all the data from users sheet
    data = users.get_all_values()
    # Set boolean to make changes within if/else statment
    sign_in = False
    # Use while loop to repeat input to user incase of error happens
    while sign_in is False:
        try:
            new_username = not_empty(f"{Fore.LIGHTYELLOW_EX} Please enter"
                                     f" a new username:\n {Style.RESET_ALL}")
            new_row = []
            # Line is column
            for line in data:
                # Column 1 is line[0] which contains the username
                if new_username == line[0]:
                    print(f"{Fore.RED} The username is already taken,"
                          f" please try again.{Style.RESET_ALL}")
                    # Allow user to enter username again.
                    new_username = not_empty(f"{Fore.LIGHTYELLOW_EX} Please "
                                             f"enter a new username:\n"
                                             f" {Style.RESET_ALL}")
                    # Ask user for the newpassword ,and confirm using input().
            new_password = not_empty(f"{Fore.LIGHTYELLOW_EX} Please enter a "
                                     "new password:\n "
                                     f"{Fore.BLACK}")
            confirm_password = input(f"{Fore.LIGHTYELLOW_EX} Please reenter "
                                     "password to confirm:\n "
                                     f"{Fore.BLACK}")
            # Call function to clear terminal
            clear_terminal()
            # If password doesnt match, the user directed back to start
            if confirm_password != new_password:
                raise ValueError(f"{Fore.RED} Passwords dont match,"
                                 f" please start again!{Style.RESET_ALL}")
            else:
                # Change boolean value of sign_in here
                sign_in = True
                print(f"{Fore.GREEN} Sign Up Succesfull{Style.RESET_ALL}")
                new_row.append(new_username)
                # Ensured the usage of hashed password using bcrypt
                # Learnt from here https://www.youtube.com/watch?v=hNa05wr0DSA
                bcrypt_byte = new_password.encode('utf-8')
                salt = bcrypt.gensalt()
                hashed_p = bcrypt.hashpw(bcrypt_byte, salt)
                new_row.append(hashed_p.decode('utf-8'))
                # Use append_row to store username and hashed password in SHEET
                users.append_row(new_row)
                user_login()
        except ValueError as error:
            print(error)


def menu_choice():
    """
    This function is called when user succesfully logs in, it
    gives user a number of options to choose from and it also allows user
    to exit the program
    """
    while True:
        # Menu has 5 options, user is returned to this menu after task.
        menu = input(f"""{Fore.LIGHTYELLOW_EX}
 Please select one of the following Options below:\n
 a - View patient details
 b - Add new patient
 c - Appointments
 d - Treatment Costs
 e - Exit
 :\n """).lower()
        clear_terminal()
        if menu == "a":
            # Insert input into file_no_pattern function to check format
            file_number = file_no_pattern(f"{Fore.LIGHTYELLOW_EX} Enter "
                                          "patient's file number."
                                          "If you dont have a no yet, please"
                                          " enter any number combination "
                                          "in the format given. "
                                          "(format: #_ _ _ _ _):\n ")
            # Define variable to call method
            patient = Patient('Patient')
            # Call patient class method patient_details()
            patient.patient_details(file_number)

        elif menu == "b":
            # Input is passed in not_empty() to make sure string
            # is not empty
            name = not_empty(f"{Fore.LIGHTYELLOW_EX} Please enter "
                             "Patient's first name:\n ")
            surname = not_empty(f"{Fore.LIGHTYELLOW_EX} Please enter"
                                " Patient's surname:\n ")
            email = validate_email()
            birthday = validate_birthdate()
            fileno = validate_fileno()
            clear_terminal()
            # List is created with arguments which pass in add_details()
            new_patient = [name, surname, email, birthday, fileno]
            patient = Patient('Patient')
            patient.add_details(new_patient)

        elif menu == "c":
            while True:
                # User has to choose between adding or viewing
                appointment_choice = input(f"""{Fore.LIGHTYELLOW_EX}
 Choose between:
 a - Add Appointment
 b - View Appointment
 :\n """)
                clear_terminal()
                if appointment_choice == "a":
                    # Get all the values from patients SHEET in google sheet
                    patient_data = patients.get_all_values()
                    file_number = file_no_pattern(f"{Fore.LIGHTYELLOW_EX} "
                                                  "Enter patient's file "
                                                  "number (format: #-----)"
                                                  " :\n ")
                    try:
                        # Use for loop to check data stored in Patients sheet
                        for num in patient_data:
                            # num[4] is column containing all file numbers
                            if file_number == num[4]:
                                # Call fxns to validate
                                date = validate_app_date()
                                time = validate_time()
                                reason = validate_treatment()
                                clear_terminal()
                                # Call add_appntmnt() method in Scheduler
                                scheduler = Scheduler()
                                scheduler.add_appntmnt(
                                    file_number,
                                    date,
                                    time,
                                    reason
                                )
                                # This is called to go back to menu
                                menu_choice()
                                break
                        else:
                            raise ValueError
                    except ValueError:
                        print(f"{Fore.RED} We dont have that file no stored,"
                              " Please add patients details first.")
                        break

                elif appointment_choice == "b":
                    # Get all data from appointments sheet.
                    appointment_data = appointments.get_all_values()
                    file_number = file_no_pattern(f"{Fore.LIGHTYELLOW_EX} "
                                                  "Enter patient's file "
                                                  "number (format: #-----)"
                                                  " :\n ")
                    try:
                        # Check if user input matches data in appointments.
                        for f_num in appointment_data:
                            # f_num[0] contains all file nos in appointments.
                            if file_number == f_num[0]:
                                clear_terminal()
                                scheduler = Scheduler()
                                scheduler.view_appointment(file_number)
                                menu_choice()
                                break
                        else:
                            raise ValueError
                    except ValueError:
                        print(f"{Fore.RED} We dont have an "
                              "appointment with that file no.")
                        break
                else:
                    print(f"{Fore.RED} Invalid option")

        elif menu == "d":
            while True:
                t_choice = input(f"""{Fore.LIGHTYELLOW_EX}
 Please Choose between
 a - Calculate Payment Due or
 b - View prices
 :\n """)
                clear_terminal()
                if t_choice == "a":
                    # Calls fxn to calculate payment due
                    payment_due()
                    break
                elif t_choice == "b":
                    # Calls fxn that displays treatment prices
                    view_treatments()
                    break
                else:
                    print(f"{Fore.RED} Invalid onput")

        elif menu == "e":
            main()

        else:
            print(f"{Fore.RED}You have entered an invalid option,"
                  " Please try again")


class Patient:
    """
    This class represents a patients, it contains methods that views
    patient details and adds patient details to same patient
    sheet in gspread.
    """
    def __init__(self, file_number):
        self.file_number = file_number

    def patient_details(self, file_number):
        """
        This method takes in file number from user and then
        displays patient details if valid file number(by checking the
        inputed file number with file number corresponding to
        patients  stored in patients datasheet in gspread), otherwise
        displays error message.
        """
        try:
            file_number_column = patients.col_values(5)
            row = file_number_column.index(file_number) + 1

            details = patients.row_values(row)
            print(f"""{Fore.YELLOW}
              ---Patient Details---
             Patient Name:{details[0].title()}
             Patient Surname:{details[1].title()}
             Email:{details[2]}
             Birthday:{details[3]}
             File Number:{details[4]}""")

        except ValueError:
            print(f"{Fore.RED} Please remember to"
                  " add patient first.")

    def add_details(self, new_patient):
        """
        Method to take in list and add each list item to
        row in patient data sheet in gspread
        """
        patients.append_row(new_patient)
        print(f"{Fore.GREEN} You've successfully added a new patient")


class Scheduler:
    """
    This class represents a scheduling system that checks if
    appointment is available, allows user to add appointment
    and show all appointments of a patient.
    """
    def __init__(self):
        self.new_appointment = []

    def is_available(self, date, time):
        """
        Method to check if inputed appointment date and time by user is
        available or not by comparing the input data with values in
        appointments
        sheet in gspread.
        """
        appointment_data = appointments.get_all_values()
        for line in appointment_data:
            if date == line[1] and time == line[2]:
                print(f"{Fore.RED} Sorry,That date and time is already booked")
                return False
        return True

    def add_appntmnt(self, file_number, date, time, reason):
        """
        Method to take in date and time if its available and
        store them with addition of file no,treatment and cost
        in a list. The list is appended to the appointment
        data sheet.
        """
        treatment_prices = treatments.row_values(2)
        treatment_names = treatments.row_values(1)
        if self.is_available(date, time):
            self.new_appointment.append(file_number)
            self.new_appointment.append(date)
            self.new_appointment.append(time)
            self.new_appointment.append(reason)
            # Used for loop to check the prices in treatments sheet.
            # Use range(len())to iterate through all treatments
            for i in range(len(treatment_names)):
                if reason == treatment_names[i]:
                    self.new_appointment.append(treatment_prices[i])
            appointments.append_row(self.new_appointment)
            print(f"{Fore.GREEN} Added appointment succesfully!")

    def view_appointment(self, file_number):
        """
        Method that displays the user a certain patient's booked
        appointments.
        This is done by take in file number as input and checking
        with corresponding details in data sheets to display an
        appropriate message to user.If inputed file number cant be found
        in data sheet , error message is shown.
        """

        file_num_column = patients.col_values(5)
        pt_row = file_num_column.index(file_number) + 1
        pt_details = patients.row_values(pt_row)
        file_num = appointments.col_values(1)
        print(f" {Fore.YELLOW}Patient {pt_details[0].title()} "
              f"{pt_details[1].title()}'s appointments")
        appointment_date = appointments.col_values(2)
        appointment_time = appointments.col_values(3)
        appointment_reason = appointments.col_values(4)
        appointment_price = appointments.col_values(5)
        number = 0
        for value in range(len(file_num)):
            if file_number == file_num[value]:
                number += 1
                print(f"""{Fore.YELLOW}
         {number}.
         Date:{appointment_date[value]}
         Time: {appointment_time[value]}
         Treatment:{appointment_reason[value].title()}
         Cost:{appointment_price[value]}€
         """)


def payment_due():
    """
    Function that allows user to choose treatments to calculate
    total payment due and displays appropriate message when given
    invalid input.
    """
    payment = False
    # Define a new list to add all the treatments user chooses
    prices = []
    while payment is False:
        # Get values from treatment sheet
        # Store each row values in different variable
        headings = treatments.row_values(1)
        costs = treatments.row_values(2)
        addition = False
        pt_treatment = input(f"""{Fore.LIGHTYELLOW_EX}
 Please a choose treatment for patient from the following options:
 {Fore.YELLOW}
 Specific Exam
 Full Oral Exam
 Filling
 Extraction
 Denture
 Cleaning
 Xray
 Root Canal
 :\n {Fore.LIGHTYELLOW_EX}""").lower()
        clear_terminal()
        # Use for loop to check if input is in headings
        for title in headings:

            if pt_treatment == title:
                u_choice = input(f"""{Fore.LIGHTYELLOW_EX}
 Choose between
 a) Add another treatment
 b) View Total Payment Due
 :\n """)
                clear_terminal()
                if u_choice == "a":
                    # Each input is added into prices list
                    prices.append(pt_treatment)
                    addition = True

                elif u_choice == "b":
                    payment = True
                    # Last input is also added to prices list
                    prices.append(pt_treatment)
                    # Find row values of treatments sheet
                    headings = treatments.row_values(1)
                    costs = treatments.row_values(2)
                    addition = True
                    # Change values in costs to integer with int()
                    # Store integers in new list
                    int_costs = [int(x) for x in costs]
                    i = 0
                    # Define a new list to add the chosen treatment's prices
                    final_list = []
                    # Use for loop to check if item in price is in headings
                    for i in prices:
                        if i in headings:
                            #  Use index() to check the treatment price
                            #  Append it to final_list
                            final_list.append(int_costs[headings.index(i)])
                    # Use sum() to add integers in list
                    print(f"{Fore.YELLOW} Total payment due"
                          f" is {sum(final_list)}")
                    # The break statement will return patient back to menu
                    break

                else:
                    print(f"{Fore.RED} Invalid option,start again")
                    addition = True
        if addition is False:
            # For when user doesnt enter a valid treatment option
            print(f"{Fore.RED} We dont have that treatment option, try again")


def view_treatments():
    """
    Function that displays the treatments and corresponding prices in
    datasheet treatments.
    """
    headings = treatments.row_values(1)
    costs = treatments.row_values(2)
    i = 0
    print(f"{Fore.YELLOW} Treatment Prices")
    # Use for loop to print out values in treatment sheet
    for i in range(len(headings)):
        print(f" {Fore.YELLOW}{headings[i].title()}:{costs[i]}€")


def validate_email():
    """
    Function that validates user's inputed email by using regular
    expressions to match pattern.
    """
    # Learnt about pattern matching and regular expression here
    # https://www.geeksforgeeks.org/pattern-matching-python-regex/
    while True:
        u_email = input(f"{Fore.LIGHTYELLOW_EX} Please enter email:\n ")
        # Use pattern matching to make sure user enter valid email
        v_email = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        # re.match checks inputed email to match v_email pattern/format
        if re.match(v_email, u_email):
            break
        else:
            print(f"{Fore.RED} Invalid email, try again")
    return u_email


def validate_app_date():
    """
    Function that takes in appointment date from user and checks if date is
    valid using datetime. It also checks if inputted date is in the
    future, and displays error message if not.
    """
    # Learnt about date time to validate dates here
    # https://stackoverflow.com/questions/16870663/how-do-i-validate-a-date-string-format-in-python
    while True:
        try:
            u_date = input(f"{Fore.LIGHTYELLOW_EX} Please add appointment"
                           " in the format DD-MM-YYYY:\n ")
            # Use datetime to check if input matches given format
            date_obj = datetime.datetime.strptime(u_date, '%d-%m-%Y')
            current_date = datetime.datetime.now()
            # Use > to check if input date is not present or past
            if date_obj > current_date:
                break
            else:
                # While loop returns user back to question
                print(f"{Fore.RED} That date is not in the future, try again.")
        except ValueError:
            print(f"{Fore.RED} That is not a valid date,try again.")
    return u_date


def validate_birthdate():
    """
    Function that validates DOB entered by user by checking if its
    a date in the past. It also checks if the user has inputted a date
    in the correct format.
    """
    while True:
        try:
            b_date = input(f"{Fore.LIGHTYELLOW_EX} Please add patient's "
                           "DOB in the format DD-MM-YYYY:\n ")
            date_item = datetime.datetime.strptime(b_date, '%d-%m-%Y')
            today_date = datetime.datetime.now()
            # Check if input date is not present or future date with <
            if date_item < today_date:
                break
            else:
                print(f"{Fore.RED} This is not a valid birthdate, try again")
        except ValueError:
            print(f"{Fore.RED} That is not a valid entry, try again")
    return b_date


def validate_time():
    """
    Function that validates appointment time user inputs using date time.
    """
    # Learnt how to validate time using date time here
    # https://stackoverflow.com/questions/33076617/how-to-validate-time-format
    while True:
        u_time = input(f"{Fore.LIGHTYELLOW_EX} Please enter time in the "
                       "format HH:MM:\n ")
        try:
            datetime.datetime.strptime(u_time, '%H:%M')
            return u_time
        except ValueError:
            print(f"{Fore.RED} Invalid time")


def validate_fileno():
    """
    Function that validates file number entered by user by checking if
    inputed file number is already in patients datasheet so that user
    doesnt add the same patient twice. If the file number is already been used,
    user is given approriate message and returned back to the menu.
    """
    patient_data = patients.get_all_values()
    while True:
        file_no = file_no_pattern(f"{Fore.LIGHTYELLOW_EX} "
                                  "Enter patient's file "
                                  "number (format: #-----)"
                                  " :\n ")
        # Use for loop to check if specific file no is already used.
        # Checked in patients sheet data.
        # Cant have the same file number again as its a unique code.
        for number in patient_data:
            if file_no == number[4]:
                print(f"{Fore.RED} This file is no is already stored.")
                menu_choice()
                break
        else:
            return file_no


def validate_treatment():
    """
    Function that validates inputed treatment to check if it is
    a treatment provided by the clinic.
    """
    treatment_headings = treatments.row_values(1)
    validate = False
    while validate is False:
        appointment_reason = input(f"""{Fore.LIGHTYELLOW_EX}
 Please a choose treatment for patient from the following options:
 {Fore.YELLOW}
 Specific Exam
 Full Oral Exam
 Filling
 Extraction
 Denture
 Cleaning
 Xray
 Root Canal:\n {Fore.LIGHTYELLOW_EX}""").lower()
        # Use forlopp to check if input is same as data in treatments
        for i in treatment_headings:
            if appointment_reason == i:
                validate = True
                break
        else:
            print(f"{Fore.RED} Invalid treatment option,try again!")

    if validate is True:
        return appointment_reason


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


def main():
    """
    This main function calls the logo function and
    choice function to start the program
    """
    logo()
    choice()


main()
