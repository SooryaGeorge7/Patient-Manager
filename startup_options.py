from colorama import Fore, Style
from utils import clear_terminal
from run import user_login, sign_up


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
