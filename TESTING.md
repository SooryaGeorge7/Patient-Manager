# Manual testing 

## Manual testing of choice() in run.py 

|Choice | Input | Expected result | Response |
|---|---|---|---|
| Please choose from options a - Log in, b - Register | a | Calls user_login() fxn | as expected |
| Please choose from options a - Log in, b - Register | b | Calls sign_up() fxn | as expected |
| Please choose from options a - Log in, b - Register | any other key | invalid input message, ask user to input again | as expected | 

## Manual testing of user_login() in run.py

|Choice | Input | Expected result | Response |
|---|---|---|---|
| Asks to enter username, password | password in database, username is not in database | gives error message, prompts user to either try login again or sign up | as expected |
| Asks to enter username, password  | username is in database, password is not in database | gives error message, prompts user to either try login again or sign up | as expected |
| Asks to enter username, password  | both username and passwords are not stored in database | gives error message, prompts user to either try login again or sign up  | as expected |
| Asks to enter username, password  | both username and passwords are stored in database | gives login successful message, calls menu_choice() | as expected |

## Manual testing of sign_up() in run.py

|Choice | Input | Expected result | Response |
|---|---|---|---|
| Asks to enter new username, new password and to confirm | Username inputted is already stored in users sheet in database | gives error message, prompts user to enter a new username again | as expected |
| Asks to enter new username, new password and to confirm | Username or password inputted is an empty string | gives error message, prompts user to enter username or password again | as expected |
| Asks to enter new username, new password and to confirm | password inputted to confirm doesn't match the password inputted initially | gives error message, prompts user to start sign up process again | as expected |
| Asks to enter new username, new password and to confirm | Enters new username, password and confirms password correctly | Gives sign up successful message and calls user_login() fxn | as expected |

## Manual testing of menu_choice() in run.py


|Choice | Input | Expected result | Response |
|---|---|---|---|
| Please choose from a - View patient details, b - Add patient details, c - Appointments, d - Treatments, e - Exit| a | Prompts user to enter patient's file number, If input valid file no, calls class Patient with method patient_details. | as expected |
| Please choose from a - View patient details, b - Add patient details, c - Appointments, d - Treatments, e - Exit | b | Prompts user to enter patient name, surname, email, date of birth and file no. If valid inputs, then calls Class patient with method add_details() | as expected |
| Please choose from a - View patient details, b - Add patient details, c - Appointments, d - Treatments, e - Exit | c | Presents user with another menu, to choose from a - add appointments, or b - view appointments | as expected | 
| Please choose from a - View patient details, b - Add patient details, c - Appointments, d - Treatments, e - Exit | d | Presents user with another menu, to choose from a - Calculate payment due, b- View prices | as expected |
| Please choose from a - View patient details, b - Add patient details, c - Appointments, d - Treatments, e - Exit | e | Returns user to start screen by calling main() | as expected |
| Please choose from a - View patient details, b - Add patient details, c - Appointments, d - Treatments, e - Exit | any other key | Invalid input error message, prompts user to enter input again | as expected |

## Manual testing of user choosing "a" in menu_choice()


|Choice | Input | Expected result | Response |
|---|---|---|---|
| Enter patient's file no | file number entered in incorrect format | input is first tested in file_no_pattern() fxn, if not valid pattern, user is returned to enter file no again| as expected |
| Enter patient's file no | valid file number format, but doesn't exist in patients sheet in spread | if valid file no format is inserted, program calls patient_details method of class Patient, in the patient_details method, it takes the file number as argument and checks if the file number corresponds to a file number in patient's sheet in gspread. If file number entered is not there, then user is given error message and asked to enter patient details before returning user to menu | as expected |
| Enter patient's file no | valid file number format that exists in patient's sheet in gspread | if valid file no format is inserted, program calls patient_details method of class Patient, in the patient_details method, it takes the file number as argument and checks if the file number corresponds to a file number in patient's sheet in gspread. If file number entered is  there, then patient details of that specific file no is displayed to user before returning user to menu | as expected | 

## Manual testing of user choosing "b" in menu_choice()


|Choice | Input | Expected result | Response |
|---|---|---|---|
| Enter patient's name, surname, email, DOB, file no | Empty strings entered for patient name or surname | empty values are passed through not_empty function to return user to enter input again if string entered was empty.| as expected |
| Enter patient's name, surname, email, DOB, file no  | Email entered is invalid | Emails inputted are passed through validate_email() fxn to check if email written matches with valid email format. User is prompt to enter email again if invalid | as expected |
| Enter patient's name, surname, email, DOB, file no | Invalid DOB format | The date of Birth entered is passed through function validate_birthdate() to check if date entered is in the correct format first before checking if DOB is not a date in the future or present. If date entered is not in correct format, then error message "This is not a valid entry" is displayed to user| as expected | 
| Enter patient's name, surname, email, DOB, file no  | Date inputted is in the future or is the present day |The date of Birth entered is passed through function validate_birthdate() to check if DOB is not a date in the future or present. If date entered is in the future, then error message "This is not a valid birthdate, try again" is displayed to user  before requesting DOB again| as expected |
| Enter patient's name, surname, email, DOB, file no | File no inputted in wrong format | File no is passed through file_no_pattern() fxn to check correct format, if not then user is promt to enter file no again | as expected | 
| Enter patient's name, surname, email, DOB, file no | File no inputted already exists in patient's sheet | A valid file no is passed through validate_fileno() fxn to check file number entered is already present in Patient's sheet in gspread, if it is already present, then error message "This file no is already added" is displayed to user before returning user to main menu | as expected | 
| Enter patient's name, surname, email, DOB, file no | All inputs entered are valid | Name, surname, email, DOB and file number is first appended to a list and add_details method of class Patient is called.The method passes the new list as its argument , which allows the values in the list to be appended to a new row in Patients sheet in gspread.


## Manual testing of user choosing "a- add appointment" after choosing option c in menu_choice()


|Choice | Input | Expected result | Response |
|---|---|---|---|
| Enter file no, appointment date, appointment time, treatment| File no entered, wrong format| File no is passed through file_no_pattern() fxn to check correct format, if not then user is prompt to enter file no again  | As expected |
| Enter file no, appointment date, appointment time, treatment| File entered doesn't have patient's details | File number entered is checked with all the file numbers stored in Patient's sheet in gspread, if it is not there, error message "We don't have that file no, Please add patient details first" is displayed to user before returning patient to main menu | As expected |
| Enter file no, appointment date, appointment time, treatment| Invalid date format | Calls validate_app_date() fxn, which first checks the format of date. If wrong format, then error message "That is not a valid date, try again." is displayed to user before asking username for date again| As expected |
| Enter file no, appointment date, appointment time, treatment| Date in the past or present day | Calls validate_app_date() fxn, which checks if valid date is in future or past. If it is in the past or is the present day, and error message "The date is not in the future" is displayed to user before asking for date again | As expected |
| Enter file no, appointment date, appointment time, treatment| Time is not in correct format | Calls validate_time() fxn, which checks the time format to be how the user is requested to insert. If invalid time format or time, an error message "Invalid time" is displayed to user before returning user to enter time again. | As expected |
| Enter file no, appointment date, appointment time, treatment| Treatment inputted is not valid| Calls validate_treatment() fxn, which checks inputted treatment with the treatments available in treatments sheet in gspread, If inputted treatment does not correspond to one of the stored treatment, then user is asked to enter treatment again after error message "Invalid treatment option, Please try again"| As expected |
| Enter file no, appointment date, appointment time, treatment| All valid inputs| Calls add_appntmnt() method of class Scheduler, which first passes date and time in method is_available() to check if that particular slot is already booked. This is done by checking the rows of appointments sheet to see if it corresponds with given date and time already. If the inputted date and time is already present in appointments sheet, then an error message "Sorry that slot is already booked" is displayed to user before returning user to menu . If appointment date and time doesn't correspond to another patient's appointment date and time in appointments sheet in g spread, then add_appntmnt() method is called to append new appointment row to appointments sheet in gspread. The treatment option is checked with treatments sheet in gspread to store the cost of treatment to appointments sheet as well with the appointment| As expected |


## Manual testing of user choosing "b- View appointments" after choosing option c in menu_choice()


|Choice | Input | Expected result | Response |
|---|---|---|---|
| Asks for patient's file no | file no wrong format |  File no is passed through file_no_pattern() fxn to check correct format, if not then user is prompt to enter file no again  | As expected |
| Asks for patient's file no| File number is not in appointments sheet| If valid file no format, Inputted file number is checked with file number stored in appointments sheet in gspread. If file no doesn't match to one in the sheet, then user is displayed error "We don't have an appointment with them, please add appointment" before returning user to add appointment| As expected |
| Asks for patient's file no| Valid input| Calls view_appointment() method of class Scheduler which checks file number with file no in patients sheet, appointments sheet to be able to display user an appropriate message showing all appointment for that specific patient. The row in appointments sheet with the inputted file no, is exported to display to user the appointment patient name, surname, date, time, treatment and cost of treatment.| As expected|

## Manual testing of user choosing "a"- Calculate total payment due after choosing option d in menu_choice()

|Choice | Input | Expected result | Response |
|---|---|---|---|
| Asks user to choose treatment from options, and then to keep adding or view payment due  | Invalid treatment option input  | in Payment_due(),If user inputs any value other than the treatment options shown to user, then error message "We don't have that treatment option, try again" is displayed to user before asking to enter treatment again. | As expected  |
| Asks user to choose treatment from options, and then to keep adding or view payment due  | User chooses an option other than "a"- add another treatment "b"- View payment due | In payment_due() and asks user is asked to add another treatment option or view total payment due. If input is neither then, error message "invalid option, start  again" is displayed before prompting user to enter treatment option again | As expected |
| Asks user to choose treatment from options, and then to keep adding or view payment due  | Valid inputs | treatment options chosen by user is added to a list which is compared to treatments in treatment sheet. If they are the same, then new list is added with the cost of treatments as integers. sum() is used to add the costs of treatment together to show payment due to user.  | As expected |


## Manual testing of user choosing "b"- View prices after choosing option d in menu_choice()

|Choice | Input | Expected result | Response |
|---|---|---|---|
| Doesn't ask any input from user |choice- b| Displays results from treatment sheet which contains the treatments and prices of each treatment in a readable manner.| As expected|

## Manual testing of user choosing option e in menu_ choice()

| Expected result | Response |
| Allows user to return to start screen | As expected |

## Manual testing of user entering invalid input in menu_ choice()

| Expected result | Response |
| Gives error message "You have entered an invalid option, please try again" before returning user to menu again| As expected |