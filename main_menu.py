"""
This is the file that contains the main menu of the application
"""
# import re
# import datetime
# import getpass
# import gspread
# from google.oauth2.service_account import Credentials
from colorama import Fore, Style
# import bcrypt
from google_sheets_api import patients, appointments
from utils import not_empty, clear_terminal, file_no_pattern
# from startup_options import logo, choice
from functions import Patient, validate_email, validate_birthdate
from functions import validate_fileno, validate_app_date, validate_time
from functions import view_treatments, Scheduler, payment_due
from functions import validate_treatment
# import run as start


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
            import run as start
            start.main()
            # exit()

        else:
            print(f"{Fore.RED}You have entered an invalid option,"
                  f" Please try again{Style.RESET_ALL}")
