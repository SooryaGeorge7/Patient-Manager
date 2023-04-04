"""
Importing libraries and data from libraries and gspread
"""
import re
import os
import datetime
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
appointement_data = appointments.get_all_values()
treatments = SHEET.worksheet('treatments')
treatments_data = treatments.get_all_values()


def clear_terminal():
    """
    Function that can be called to clear terminal at any stage of the program
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def sign_up():
    """
    Function that allows user to sign in when user chooses to.
    It allows user to input username and password.
    Checks that the username is not taken already and allows
    username to confirm password and displays error message if user
    gives in an invalid username or if passwords dont match.
    """
    data = users.get_all_values()
    sign_in = False
    while sign_in is False:
        try:
            new_username = input(f"{Fore.LIGHTYELLOW_EX} Please enter"
                                 " a new username:\n ")
            new_row = []
            for line in data:
                if new_username == line[0]:
                    print(f"{Fore.RED} The username is already taken,"
                          " please try again.")
                    # Allow user to enter username again.
                    new_username = not_empty(f"{Fore.LIGHTYELLOW_EX} Please "
                                             "enter a new username:\n ")
                    # Ask user for the newpassword ,and confirm using input().
            new_password = not_empty(" Please enter a new password:\n ")
            confirm_password = input(" Please reenter password to confirm:\n ")
            clear_terminal()
            if confirm_password != new_password:
                raise ValueError(f"{Fore.RED} Passwords dont match,"
                                 " please start again!")
            else:
                sign_in = True
                print(f"{Fore.GREEN} Sign Up Succesfull{Style.RESET_ALL}")
                new_row.append(new_username)
                # Ensured the usage of hashed password using bcrypt
                # Learnt from here https://www.youtube.com/watch?v=hNa05wr0DSA
                bcrypt_byte = new_password.encode('utf-8')
                salt = bcrypt.gensalt()
                hashed_p = bcrypt.hashpw(bcrypt_byte, salt)
                new_row.append(hashed_p.decode('utf-8'))
                users.append_row(new_row)
                user_login()
        except ValueError as error:
            print(error)


def file_no_pattern(user_text):
    while True:
        user_pattern = input(user_text)
        file_pattern = r"^#[0-9]{5}$"
        if re.match(file_pattern, user_pattern):
            return user_pattern
        else:
            print(f"{Fore.RED} You have not entered a valid file no.")


class Patient:
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
            view_patient = print(f"""{Fore.YELLOW}
              ---Patient Details---
             Patient Name:{details[0]}
             Patient Surname:{details[1]}
             Email:{details[2]}
             Birthday:{details[3]}
             File Number:{details[4]}""")
            return view_patient
        except ValueError:
            print(f"{Fore.RED} File does'nt exist")

    def add_details(self, new_patient):
        """
        Method to take in list and add each list item to
        row in patient data sheet in gspread
        """
        patients.append_row(new_patient)
        added = print(f"{Fore.GREEN} You've successfully added a new patient")

        return added


class Scheduler:
    def __init__(self):
        self.new_appointment = []

    def is_available(self, date, time):
        """
        Method to check if inputed appointment date and time by user is
        available or not by comparing the input data with values in
        appointments
        sheet in gspread.
        """
        for line in appointement_data:
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
        try:
            file_num_column = patients.col_values(5)
            pt_row = file_num_column.index(file_number) + 1
            pt_details = patients.row_values(pt_row)
            file_num = appointments.col_values(1)
            print(f" {Fore.YELLOW}Patient {pt_details[0]} {pt_details[1]}'s"
                  " appointments")
            appointment_date = appointments.col_values(2)
            appointment_time = appointments.col_values(3)
            appointment_reason = appointments.col_values(4)
            appointment_price = appointments.col_values(5)
            for value in range(len(file_num)):
                if file_number == file_num[value]:
                    view_date = print(f"""{Fore.YELLOW}
 {appointment_date[value]}at {appointment_time[value]} hours
 Treatment:{appointment_reason[value]}
 Cost:{appointment_price[value]}
 """)
            return view_date
        except ValueError:
            print(f"{Fore.RED} We dont have an appointment"
                  " with that file number")


def payment_due():
    """
    Function that allows user to choose treatments to calculate
    total payment due and displays appropriate message when given
    invalid input.
    """
    payment = False
    prices = []
    while payment is False:
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
 :\n """).lower()
        clear_terminal()
        for a in headings:

            if pt_treatment == a:
                u_choice = input(f"""{Fore.LIGHTYELLOW_EX}
 Choose between
 a) Add another treatment
 b) Total Payment Due
 :\n """)
                clear_terminal()
                if u_choice == "a":
                    prices.append(pt_treatment)
                    addition = True

                elif u_choice == "b":
                    payment = True
                    prices.append(pt_treatment)
                    headings = treatments.row_values(1)
                    costs = treatments.row_values(2)
                    addition = True

                    int_costs = [int(x) for x in costs]
                    i = 0
                    final_list = []
                    for i in prices:
                        if i in headings:
                            final_list.append(int_costs[headings.index(i)])
                    print(f"{Fore.YELLOW} Total payment due"
                          f" is {sum(final_list)}")
                    break

                else:
                    print(f"{Fore.RED} invalid option,start again")
                    addition = True
        if addition is False:
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
    for i in range(len(headings)):
        treatment_costs = print(f" {Fore.YELLOW}{headings[i]}:{costs[i]}")
    return treatment_costs


def validate_email():
    """
    Function that validates user's inputed email by using regular
    expressions to match pattern.
    """
    while True:
        u_email = input(f"{Fore.LIGHTYELLOW_EX} Please enter email:\n ")
        v_email = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
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
    while True:
        try:
            u_date = input(f"{Fore.LIGHTYELLOW_EX} Please add appointment"
                           " in the format DD-MM-YYYY:\n ")
            date_obj = datetime.datetime.strptime(u_date, '%d-%m-%Y')
            current_date = datetime.datetime.now()
            if date_obj > current_date:
                break
            else:
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
        for number in patient_data:
            if file_no == number[4]:
                print(f"{Fore.RED} This patient is already added.")
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
        appointment_reason = input(f"""{Fore.YELLOW}
 Please a choose treatment for patient from the following options:
 Specific Exam
 Full Oral Exam
 Filling
 Extraction
 Denture
 Cleaning
 Xray
 Root Canal:\n """).lower()
        for i in treatment_headings:
            if appointment_reason == i:
                validate = True
                break
        else:
            print(f"{Fore.RED} Invalid treatment option,try again!")

    if validate is True:
        return appointment_reason


def not_empty(user_text):
    while True:
        user_input = input(user_text)
        if len(user_input) == 0:
            print(f"{Fore.RED} You've entered an empty string")
        else:
            return user_input


def user_login():
    """
    Function that allows user to enter username and password
    and validates them by checking with the usernames and passwords stored
    users data sheet. The inputed password has to encoded to check with
    the hashed passwords in data sheet.(You have to encode the passwords
    in datasheet because they were decoded when being stored.)
    """
    data = users.get_all_values()
    log_in = False
    print(f"{Fore.GREEN} You may log in!")
    while log_in is False:
        login_username = input(f"{Fore.LIGHTYELLOW_EX} Please "
                               "enter username:\n ")
        login_password = input(" Please enter password:\n ")
        coded_password = login_password.encode('utf-8')
        clear_terminal()
        try:
            for x in data:
                username = x[0]
                password = x[1]
                hash_password = password.encode('utf-8')

                if login_username == username and \
                   bcrypt.checkpw(coded_password, hash_password):
                    print(f"{Fore.GREEN} Log in Successful!")
                    menu_choice()
                    break

            else:
                user_option = input(f"""{Fore.RED}
 We dont have those credentials,
 Please choose between":
 {Fore.LIGHTYELLOW_EX}
 a - Try Log in again
 b - Register
 :\n """)
                if user_option == "a":
                    clear_terminal()
                    raise ValueError
                elif user_option == "b":
                    clear_terminal()
                    sign_up()
                    break
                else:
                    print(f"{Fore.RED} Invalid option.Start again")
        except ValueError:
            print(f"{Fore.RED} Please try again")


def menu_choice():
    """
    This function is called when user succesfully logs in, it
    gives user a number of options to choose from and it also allows user
    to exit the program
    """
    while True:
        menu = input(f"""{Fore.LIGHTYELLOW_EX}
 Please select one of the following Options below:\n
 a - View patient details
 b - Add new patient
 c - Appointment
 d - Treatment Costs
 e - Exit
 :\n """).lower()
        clear_terminal()
        if menu == "a":
            file_number = file_no_pattern(f"{Fore.LIGHTYELLOW_EX} Enter "
                                          "patient's file number"
                                          "(format: #_ _ _ _ _):\n ")
            patient = Patient('Patient')
            patient.patient_details(file_number)

        elif menu == "b":
            name = not_empty(" Please enter Patient's first name:\n ")
            surname = not_empty(" Please enter Patient's surname:\n ")
            email = validate_email()
            birthday = validate_birthdate()
            fileno = validate_fileno()
            clear_terminal()
            new_patient = [name, surname, email, birthday, fileno]

            patient = Patient('Patient')
            patient.add_details(new_patient)

        elif menu == "c":
            while True:
                appointment_choice = input(f"""{Fore.LIGHTYELLOW_EX}
 Choose between:
 a) Add Appointment
 b) View Appointment
 :\n """)
                clear_terminal()
                if appointment_choice == "a":
                    patient_data = patients.get_all_values()
                    file_number = file_no_pattern(f"{Fore.LIGHTYELLOW_EX} "
                                                  "Enter patient's file "
                                                  "number (format: #-----)"
                                                  " :\n ")
                    try:
                        for num in patient_data:
                            if file_number == num[4]:
                                date = validate_app_date()
                                time = validate_time()
                                reason = validate_treatment()
                                scheduler = Scheduler()
                                scheduler.add_appntmnt(
                                    file_number,
                                    date,
                                    time,
                                    reason
                                )
                                menu_choice()
                                break
                        else:
                            raise ValueError
                    except ValueError:
                        print(f"{Fore.RED} We dont have that file no,"
                              " Please add patients details first.")
                        break

                elif appointment_choice == "b":
                    file_number = file_no_pattern(f"{Fore.LIGHTYELLOW_EX} "
                                                  "Enter patient's file "
                                                  "number (format: #-----)"
                                                  " :\n ")
                    scheduler = Scheduler()
                    scheduler.view_appointment(file_number)
                    break
                else:
                    print(f"{Fore.RED} invalid option!")

        elif menu == "d":
            while True:
                t_choice = input("""
 Please Choose between
 a) Calculate Total Cost
 b) View prices
 :\n """)
                clear_terminal()
                if t_choice == "a":
                    payment_due()
                    break
                elif t_choice == "b":
                    view_treatments()
                    break
                else:
                    print(f"{Fore.RED} invalid input")

        elif menu == "e":
            main()

        else:
            print(f"{Fore.RED}You have entered an invalid option,"
                  " Please try again")


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
 Choice:\n """)
        clear_terminal()
        if user_choice == "a":
            option = True
            user_login()
        elif user_choice == "b":
            sign_up()
            option = True

        else:
            print(f"{Fore.RED} Invalid option, try again")


def main():
    """
    This main function calls the logo function and
    choice function to start the program
    """
    logo()
    choice()


main()
