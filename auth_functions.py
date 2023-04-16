"""
This is the file that runs the login and signup functions
"""
# Learnt how to make password invisible with get pass here:
# https://stackoverflow.com/questions/9202224/getting-a-hidden-password-input
# Learnt how to hash passwords here:
# https://stackoverflow.com/questions/63387149/hashing-a-password-with-bcrypt
# https://www.youtube.com/watch?v=hNa05wr0DSA&t=679s
import getpass
from colorama import Fore, Style
import bcrypt
from utils import not_empty, clear_terminal
from google_sheets_api import users
import main_menu as menu


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
                    menu.menu_choice()
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
                # Calls fxn to allow user to login after signing up
                user_login()
        except ValueError as error:
            print(error)
