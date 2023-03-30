import re
import os
import datetime
import gspread
from google.oauth2.service_account import Credentials
from colorama import Fore, Style

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
    os.system('cls' if os.name == 'nt' else 'clear')


def sign_up():
    data = users.get_all_values()
    sign_in = False
    while sign_in is False:
        try:
            new_username = input("Please enter a new username:\n")
            new_row = []
            for line in data:
                if new_username == line[0]:
                    print(f""""
                    {Fore.RED}The username is already taken, please try again.""")
                    # allow user to enter username again.
                    new_username = input("Please enter a new username:\n")
                    # ask user for the newpassword ,and confirm using input().
            new_password = input("Please enter a new password:\n")
            confirm_password = input("Please reenter password to confirm:\n")
            clear_terminal()
            if confirm_password != new_password:
                raise ValueError(f"""
                {Fore.RED}Passwords dont match, please start again!""")
            else:
                sign_in = True
                print(f"{Fore.GREEN}Sign Up Succesfull{Style.RESET_ALL}")
                new_row.append(new_username)
                new_row.append(new_password)
                users.append_row(new_row)
                user_login()
        except ValueError as error:
            print(error)


class Patient:
    def __init__(self, file_number):
        self.file_number = file_number

    def patient_details(self, file_number):
        try:
            file_number_column = patients.col_values(5)
            row = file_number_column.index(file_number) + 1

            details = patients.row_values(row)
            view_patient = print(f"""{Fore.YELLOW}
---Patient Details---
Patient Name:{details[0]}
Patient Surname:{details[1]}\nEmail:{details[2]}
Birthday:{details[3]}\nFile Number:{details[4]}""")
            return view_patient
        except ValueError:
            print(f"{Fore.RED}File does'nt exist")

    def add_details(self, new_patient):
        patients.append_row(new_patient)
        added = print(f"{Fore.GREEN}You've successfully added a new patient")

        return added


class Scheduler:
    def __init__(self):
        self.new_appointment = []

    def is_available(self, date, time):
        for line in appointement_data:
            if date == line[1] and time == line[2]:
                print(f"{Fore.RED}Sorry, that date and time is already booked")
                return False
        return True

    def add_appntmnt(self, file_number, date, time):
        if self.is_available(date, time):
            self.new_appointment.append(file_number)
            self.new_appointment.append(date)
            self.new_appointment.append(time)
            appointments.append_row(self.new_appointment)
            print(f"{Fore.GREEN}Added appointment succesfully!")

    def view_appointment(self, file_number):
        try:
            file_num_column = patients.col_values(5)
            pt_row = file_num_column.index(file_number) + 1
            pt_details = patients.row_values(pt_row)
            file_num = appointments.col_values(1)
            print(f"""
Patient {pt_details[0]} {pt_details[1]}'s appointments""")
            appointment_date = appointments.col_values(2)
            appointment_time = appointments.col_values(3)
            for value in range(len(file_num)):
                if file_number == file_num[value]:
                    view_date = print(f"""{Fore.YELLOW}
{appointment_date[value]}at {appointment_time[value]} hours
""")
            return view_date
        except ValueError:
            print(f"{Fore.RED}We dont have an appointment with that file number")


def payment_due():
    payment = False
    prices = []
    while payment is False:
        headings = treatments.row_values(1)
        costs = treatments.row_values(2)
        addition = False
        pt_treatment = input(f'''{Fore.YELLOW}Please a choose treatment for patient
from the following options:
Specific Exam
Full Oral Exam
Filling
Extraction
Denture
Cleaning
Xray
Root Canal
:\n''').lower()
        clear_terminal()
        for a in headings:
            
            if pt_treatment == a:
                u_choice = input('''Choose between
a) Add another treatment
b) Total Payment Due
:\n''')
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
                    print(f"""{Fore.YELLOW}Total payment due is {sum(final_list)}""")
                    
                    break

                else:
                    print(f"{Fore.RED}invalid option,start again")
                    
                    addition = True
                       

        if addition is False:
            print(f"{Fore.RED}We dont have that treatment option, try again")


def view_treatments():

    headings = treatments.row_values(1)
    costs = treatments.row_values(2)
    i = 0
    print("Treatment Prices")
    for i in range(len(headings)):
        treatment_costs = print(f"{Fore.YELLOW}{headings[i]}:{costs[i]}")
    return treatment_costs


def validate_email():
    while True:
        u_email = input("Please enter email:\n")
        v_email = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if re.match(v_email, u_email):
            break
        else:
            print(f"{Fore.RED}Invalid email, try again")
    return u_email


def validate_app_date():
    while True:
        try:
            u_date = input("Please add appointment in the format DD-MM-YYYY:\n")
            date_obj = datetime.datetime.strptime(u_date, '%d-%m-%Y')
            current_date = datetime.datetime.now()
            if date_obj > current_date:
                break
            else:
                print(f"{Fore.RED}That date is not in the future, try again")
        except ValueError:
            print(f"{Fore.RED}That is not a valid date,try again")
    return u_date


def validate_birthdate():
    while True:
        try:
            b_date = input("Please add patient's DOB in the format DD-MM-YYYY:\n")
            date_item = datetime.datetime.strptime(b_date, '%d-%m-%Y')
            today_date = datetime.datetime.now()
            if date_item < today_date:
                break
            else:
                print(f"{Fore.RED}This is not a valid birthdate, try again")
        except ValueError:
            print(f"{Fore.RED}That is not a valid entry, try again")
    return b_date


def validate_time():
    while True:
        u_time = input("Please enter time in the format HH:MM:\n")
        try:
            datetime.datetime.strptime(u_time, '%H:%M')
            return u_time
        except ValueError:
            print(f"{Fore.RED}invalid time")

def validate_fileno():
    patient_data = patients.get_all_values()
    while True:
        file_no = input("Please enter patient's file number:\n")
        for number in patient_data:
            if file_no == number[4]:
                print("This patient is already added")
                menu_choice()
                
                break
        else:
            return file_no


def user_login():
    data = users.get_all_values()
    log_in = False
    print(f"{Fore.LIGHTYELLOW_EX}You may log in!")
    while log_in is False:
        login_username = input("Please enter username: \n")
        login_password = input("Please enter password: \n")
        clear_terminal()
        try:
            for x in data:
                username = x[0]
                password = x[1]

                if login_username == username and login_password == password:
                    print(f"{Fore.GREEN}Log in Successful!")
                    menu_choice()
                    
                    break

            else:
                raise ValueError
        except ValueError:
            print(f"""
{Fore.RED}You've entered invalid credentials,Please try again
""")

def menu_choice():
    while True:
        menu = input(f'''{Fore.LIGHTYELLOW_EX}
Please select one of the following Options below:\n
a - View patient details
b - Add new patient
c - Appointment
d - Treatment Costs
e - Exit
: \n''').lower()
        clear_terminal()
        if menu == "a":
            file_number = input("Enter patient's file number(eg:#76654): \n")
            patient = Patient('Patient')
            patient.patient_details(file_number)
            

        elif menu == "b":
            name = input("Please enter Patient's first name:\n")
            surname = input("Please enter Patient's surname:\n")
            email = validate_email()
            birthday = validate_birthdate()
            fileno = validate_fileno()
            clear_terminal()
            new_patient = [name, surname, email, birthday, fileno]

            patient = Patient('Patient')
            patient.add_details(new_patient)
            

        elif menu == "c":
            while True:
                appointment_choice = input('''Choose between
 a) Add Appointment
 b) View Appointment
 :\n''')
                clear_terminal()
                if appointment_choice == "a":
                    patient_data = patients.get_all_values()
                    file_number = input("Please enter file number:\n")
                    try:
                        for num in patient_data:
                            if file_number == num[4]:
                                date = validate_app_date()
                                time = validate_time()
                                scheduler = Scheduler()
                                scheduler.add_appntmnt(file_number, date, time)
                                menu_choice()
                                break
                        else:
                            raise ValueError
                    except ValueError:
                        print(f'''{Fore.RED}
We dont have that file no, Please add patients details first''')
                        break

                elif appointment_choice == "b":
                    file_number = input("Enter patient's file number: \n")
                    scheduler = Scheduler()
                    scheduler.view_appointment(file_number)
                    break
                else:
                    print(f"{Fore.RED}invalid option!")

        elif menu == "d":
            while True:
                t_choice = input('''Please Choose between
a) Calculate Total Cost
b) View prices
:\n''')
                clear_terminal()
                if t_choice == "a":
                    payment_due()
                    break
                elif t_choice == "b":
                    view_treatments()
                    break
                else:
                    print(f"{Fore.RED}invalid input")

        elif menu == "e":
            print(f"{Fore.BLUE}Goodbye")
            exit()

        else:
            print(f"""
{Fore.RED}You have entered an invalid option, Please try again
""")

def logo():

    print(f"""{Fore.CYAN}
    _______         _    _                  _                  
   |_   __ \       / |_ (_)                / |_                
     | |__) |,--. `| |-'__  .---.  _ .--. `| |-'               
     |  ___/`'_\ : | | [  |/ /__\\[ `.-. | | |                 
    _| |_   // | |,| |, | || \__., | | | | | |,                
   |_____|  \'-;__/\__/[___]'.__.'[___||__]\__/                
    ____    ____                                               
   |_   \  /   _|                                              
     |   \/   |   ,--.   _ .--.   ,--.   .--./) .---.  _ .--.  
     | |\  /| |  `'_\ : [ `.-. | `'_\ : / /'`\;/ /__\\[ `/'`\] 
    _| |_\/_| |_ // | |, | | | | // | |,\ \._//| \__., | |     
   |_____||_____|\'-;__/[___||__]\'-;__/.',__`  '.__.'[___]    
                                       ( ( __))                
    """)
    print(f"""{Fore.BLUE}
    Welcome to Patient Manager.
    The system to manage patients in your practice.
    {Style.RESET_ALL}""")



def choice():
    option = False
    while option is False:
        user_choice = input(f'''{Fore.LIGHTYELLOW_EX}Please choose from options below:
a) Log in
b) Register
Choice: \n''')
        clear_terminal()
        if user_choice == "a":
            option = True
            user_login()
        elif user_choice == "b":
            sign_up()
            option = True

        else:
            print(f"{Fore.RED}Invalid option, try again")


def main():
    logo()
    choice()


main()
