import re
import datetime
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

appointments = SHEET.worksheet('appointments')
appointement_data = appointments.get_all_values()

treatments = SHEET.worksheet('treatments')
treatments_data = treatments.get_all_values()


def sign_up():
    sign_in = False
    while sign_in is False:
        try:
            new_username = input("Please enter a new username:\n")
            new_row = []
            for line in data:
                if new_username == line[0]:
                    print("The username is already taken, please try again.")
                    # allow user to enter username again.
                    new_username = input("Please enter a new username:\n")
                    # ask user for the newpassword ,and confirm using input().
            new_password = input("Please enter a new password:\n")
            confirm_password = input("Please reenter password to confirm:\n")

            if confirm_password != new_password:
                raise ValueError("Passwords dont match, please try again!")
            else:
                sign_in = True
                print("Sign Up Succesfull")
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
            view_patient = print(f"""
---Patient Details---
Patient Name:{details[0]}
Patient Surname:{details[1]}\nEmail:{details[2]}
Birthday:{details[3]}\nFile Number:{details[4]}""")
            return view_patient
        except ValueError:
            print("File does'nt exist, Try again")

    def add_details(self, new_patient):
        patients.append_row(new_patient)
        added = print("You've successfully added a new patient")

        return added


class Scheduler:
    def __init__(self):
        self.new_appointment = []

    def is_available(self, date, time):
        for line in appointement_data:
            if date == line[1] and time == line[2]:
                print("Sorry, that date and time is already booked")
                return False
        return True

    def add_appointment(self, file_number, date, time):
        if self.is_available(date, time):
            self.new_appointment.append(file_number)
            self.new_appointment.append(date)
            self.new_appointment.append(time)
            appointments.append_row(self.new_appointment)
            print("Added appointment succesfully!")

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
                    view_date = print(f"""
{appointment_date[value]}at {appointment_time[value]} hours
""")
            return view_date
        except ValueError:
            print("We dont have an appointment with that file number")


def payment_due():
    payment = False
    prices = []
    while payment is False:
        headings = treatments.row_values(1)
        costs = treatments.row_values(2)
        addition = False
        pt_treatment = input('''Please a choose treatment for patient
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
        for a in headings:
            if pt_treatment == a:
                u_choice = input('''Choose between
a) Add another treatment
b) Total Payment Due
:\n''')
                if u_choice == "a":
                    prices.append(pt_treatment)
                    addition = True

                elif u_choice == "b":
                    payment = True
                    prices.append(pt_treatment)
                    print(prices)
                    headings = treatments.row_values(1)
                    costs = treatments.row_values(2)
                    addition = True

                    int_costs = [int(x) for x in costs]
                    print(int_costs)
                    i = 0
                    final_list = []
                    for i in prices:
                        if i in headings:
                            final_list.append(int_costs[headings.index(i)])
                    print(f"""Total payment due is {sum(final_list)}""")
                    # print(sum(int_costs))
                    break

                else:
                    print("invalid option")

        if addition is False:
            print("We dont have that treatment option, try again")


def view_treatments():

    headings = treatments.row_values(1)
    costs = treatments.row_values(2)
    i = 0
    print("Treatment Prices")
    for i in range(len(headings)):
        treatment_costs = print(f"{headings[i]}:{costs[i]}")
    return treatment_costs


def validate_email():
    while True:
        u_email = input("Please enter email")
        v_email = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if re.match(v_email, u_email):
            print("Valid Email")
            break
        else:
            print("Invalid email, try again")
    return u_email


def validate_app_date():
    while True:
        u_date = input("Please add appointment date")
        date_obj = datetime.datetime.strptime(u_date, '%d-%m-%Y')
        current_date = datetime.datetime.now()
        if date_obj > current_date:
            print("Valid date entry")
            break
        else:
            print("That date is not in the future, try again")
    return u_date


def validate_birthdate():
    while True:
        b_date = input("Please enter patient's Birthdate")
        date_item = datetime.datetime.strptime(b_date, '%d-%m-%Y')
        today_date = datetime.datetime.now()
        if date_item < today_date:
            print("valid birthdate")
            break
        else:
            print("This is not a valid birthdate, try again")
    return b_date


def validate_time():
    while True:
        u_time = input("Please enter time")
        try:
            datetime.datetime.strptime(u_time, '%H:%M')
            return u_time
        except ValueError:
            print("invalid time")


def user_login():
    log_in = False
    print("You may log in!")
    while log_in is False:
        login_username = input("Please enter username: \n")
        login_password = input("Please enter password: \n")
        try:
            for x in data:
                username = x[0]
                password = x[1]

                if login_username == username and login_password == password:
                    log_in = True
                    print("Log in Successful!")
                    break
                elif login_username != username and login_password == password:
                    print("You've entered an invalid username ")

                elif login_username == username and login_password != password:
                    print("Your password is incorrect ")

            else:
                raise ValueError
        except ValueError:
            print("try again")

    while log_in is True:
        menu = input('''\n Please select one of the following Options below:\n
a - View patient details
b - Add new patient
c - Appointment
d - Treatment Costs
e - Exit
: \n''').lower()
        if menu == "a":
            file_number = input("Enter patient's file number(eg:#76654): \n")
            patient = Patient('Patient')
            patient.patient_details(file_number)

        elif menu == "b":
            name = input("Please enter Patient's first name:\n")
            surname = input("Please enter Patient's surname:\n")
            email = validate_email()
            birthday = validate_birthdate()
            fileno = input("Please enter patient's file number:\n")
            new_patient = [name, surname, email, birthday, fileno]

            patient = Patient('Patient')
            patient.add_details(new_patient)

        elif menu == "c":
            appointment_choice = input('''Choose between
 a) Add Appointment
 b) View Appointment
 :\n''')
            if appointment_choice == "a":
                file_number = input("Please enter file number:\n")
                try:
                    for num in patient_data:
                        if file_number == num[4]:
                            date = validate_app_date()
                            time = validate_time()
                            scheduler = Scheduler()
                            scheduler.add_appointment(file_number, date, time)
                            break
                    else:
                        raise ValueError
                except ValueError:
                    print('''
We dont have that file no, Please add patients details first''')

            elif appointment_choice == "b":
                file_number = input("Enter patient's file number: \n")
                scheduler = Scheduler()
                scheduler.view_appointment(file_number)
            else:
                print("invalid input!")

        elif menu == "d":
            t_choice = input('''Please Choose between
a) Calculate Total Cost
b) View prices
:\n''')
            if t_choice == "a":
                payment_due()
            elif t_choice == "b":
                view_treatments()
            else:
                print("invalid input")

        elif menu == "e":
            print("Goodbye")
            exit()

        else:
            print("You have entered an invalid option, Please try again")


def choice():
    option = False
    while option is False:
        user_choice = input('''Please choose from options below:
a) Log in
b) Register
Choice: \n''')
        if user_choice == "a":
            option = True
            user_login()
        elif user_choice == "b":
            sign_up()
            option = True

        else:
            print("Invalid option, try again")


def main():
    choice()


main()
