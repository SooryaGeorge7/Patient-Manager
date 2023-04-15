"""
Importing libraries and data from libraries and gspread
"""
import re
import datetime
# import getpass
import gspread
from google.oauth2.service_account import Credentials
from colorama import Fore, Style
# import bcrypt
from utils import not_empty, clear_terminal, file_no_pattern
from startup_options import logo, choice

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
 :\n {Style.RESET_ALL}""").lower()
        clear_terminal()
        if menu == "a":
            # Insert input into file_no_pattern function to check format
            file_number = file_no_pattern(f"{Fore.LIGHTYELLOW_EX} Enter "
                                          "patient's file number."
                                          "If you dont have a no yet, please"
                                          " enter any number combination "
                                          "in the format given. "
                                          "(format: #_ _ _ _ _):\n "
                                          f"{Style.RESET_ALL}")
            # Define variable to call method
            patient = Patient('Patient')
            # Call patient class method patient_details()
            patient.patient_details(file_number)

        elif menu == "b":
            # Input is passed in not_empty() to make sure string
            # is not empty
            name = not_empty(f"{Fore.LIGHTYELLOW_EX} Please enter "
                             f"Patient's first name:\n {Style.RESET_ALL}")
            surname = not_empty(f"{Fore.LIGHTYELLOW_EX} Please enter"
                                " Patient's surname:\n "
                                f"{Style.RESET_ALL}")
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
 :\n {Style.RESET_ALL}""")
                clear_terminal()
                if appointment_choice == "a":
                    # Get all the values from patients SHEET in google sheet
                    patient_data = patients.get_all_values()
                    file_number = file_no_pattern(f"{Fore.LIGHTYELLOW_EX} "
                                                  "Enter patient's file "
                                                  "number (format: #-----)"
                                                  f" :\n {Style.RESET_ALL}")
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
                              " Please add patients details first."
                              f"{Style.RESET_ALL}")
                        break

                elif appointment_choice == "b":
                    # Get all data from appointments sheet.
                    appointment_data = appointments.get_all_values()
                    file_number = file_no_pattern(f"{Fore.LIGHTYELLOW_EX} "
                                                  "Enter patient's file "
                                                  "number (format: #-----)"
                                                  " :\n "
                                                  f"{Style.RESET_ALL}")
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
                              "appointment with that file no."
                              f"{Style.RESET_ALL}")
                        break
                else:
                    print(f"{Fore.RED} Invalid option{Style.RESET_ALL}")

        elif menu == "d":
            while True:
                t_choice = input(f"""{Fore.LIGHTYELLOW_EX}
 Please Choose between
 a - Calculate Payment Due or
 b - View prices
 :\n {Style.RESET_ALL}""")
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
                    print(f"{Fore.RED} Invalid onput{Style.RESET_ALL}")

        elif menu == "e":
            main()

        else:
            print(f"{Fore.RED}You have entered an invalid option,"
                  f" Please try again{Style.RESET_ALL}")


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
 :\n {Style.RESET_ALL}""").lower()
        clear_terminal()
        # Use for loop to check if input is in headings
        for title in headings:

            if pt_treatment == title:
                u_choice = input(f"""{Fore.LIGHTYELLOW_EX}
 Choose between
 a) Add another treatment
 b) View Total Payment Due
 :\n {Style.RESET_ALL}""")
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
        u_email = input(f"{Fore.LIGHTYELLOW_EX} Please enter email:\n"
                        f" {Style.RESET_ALL}")
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
                           f" in the format DD-MM-YYYY:\n {Style.RESET_ALL}")
            # Use datetime to check if input matches given format
            date_obj = datetime.datetime.strptime(u_date, '%d-%m-%Y')
            current_date = datetime.datetime.now()
            # Use > to check if input date is not present or past
            if date_obj > current_date:
                break
            else:
                # While loop returns user back to question
                print(f"{Fore.RED} That date is not in the future, try again."
                      f"{Style.RESET_ALL}")
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
                           "DOB in the format DD-MM-YYYY:\n "
                           f"{Style.RESET_ALL}")
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
                       f"format HH:MM:\n {Style.RESET_ALL}")
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
                                  f" :\n {Style.RESET_ALL}")
        # Use for loop to check if specific file no is already used.
        # Checked in patients sheet data.
        # Cant have the same file number again as its a unique code.
        for number in patient_data:
            if file_no == number[4]:
                print(f"{Fore.RED} This file no is already stored."
                      f"{Style.RESET_ALL}")
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
 Root Canal:\n {Style.RESET_ALL}""").lower()
        # Use forlopp to check if input is same as data in treatments
        for i in treatment_headings:
            if appointment_reason == i:
                validate = True
                break
        else:
            print(f"{Fore.RED} Invalid treatment option,try again!")

    if validate is True:
        return appointment_reason


def main():
    """
    This main function calls the logo function and
    choice function to start the program
    """
    logo()
    choice()


main()
