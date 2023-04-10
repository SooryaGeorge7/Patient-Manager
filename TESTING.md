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
| Asks to enter username, password  | both username and passwords are stored in database | gives login succesful message, calls menu_choice() | as expected |

## Manual testing of sign_up() in run.py

|Choice | Input | Expected result | Response |
|---|---|---|---|
| Asks to enter new username, new password and to confirm | Username inputed is already stored in users sheet in database | gives error message, prompts user to enter a new username again | as expected |
| Asks to enter new username, new password and to confirm | Username or password inputed is an empty string | gives error message, prompts user to enter username or password again | as expected |
| Asks to enter new username, new password and to confirm | password inputed to confirm doesnt match the password inputed initially | gives error message, prompts user to start sign up process again | as expected |
| Asks to enter new username, new password and to confirm | Enters new username, password and confirms password correctly | Gives sign up succesful message and calls user_login() fxn | as expected |

## Manual testing of menu_choice() in run.py


|Choice | Input | Expected result | Response |
|---|---|---|---|
| Please choose from a - View patient details, b - Add patient details, c - Appointments, d - Treatments, e - Exit| a | Prompts user to enter pt's file number, If input valid file no, calls class Patient with method patient_details. | as expected |
| Please choose from a - View patient details, b - Add patient details, c - Appointments, d - Treatments, e - Exit | b | Prompts user to enter patient name, surname, email, date of birth and file no. If valid inputs, then calls Class patient with method add_details() | as expected |
| Please choose from a - View patient details, b - Add patient details, c - Appointments, d - Treatments, e - Exit | c | Presents user with another menu, to choose from a - add appointments, or b - view appointments | as expected | 
| Please choose from a - View patient details, b - Add patient details, c - Appointments, d - Treatments, e - Exit | d | Presents user with another menu, to choose from a - Calculate payment due, b- View prices | as expected |
| Please choose from a - View patient details, b - Add patient details, c - Appointments, d - Treatments, e - Exit | e | Returns user to start screen by calling main() | as expected |
| Please choose from a - View patient details, b - Add patient details, c - Appointments, d - Treatments, e - Exit | any other key | Invalid input error message, prompts user to enter input again | as expected |

## Manual testing of user choosing "a" in menu_choice()
|Choice | Input | Expected result | Response |
|---|---|---|---|
| Enter patient's file no | file number entered in incorrect format | input is first tested in file_no_pattern() fxn, if not valid pattern, user is returned to enter file no again| as expected |
| Enter patient's file no | valid file number format, but doesnt exist in patients sheet in spread | if valid file no format is inserted, program calls patient_details method of class Patient, in the patient_details method, it takes the file number as argument and checks if the file number corresponds to a file number in patient's sheet in gspread. If file number entered is not there, then user is given error message and asked to enter patient details before returning user to menu | as expected |
| Enter patient's file no | valif file number format that exists in patient's sheet in gspread | if valid file no format is inserted, program calls patient_details method of class Patient, in the patient_details method, it takes the file number as argument and checks if the file number corresponds to a file number in patient's sheet in gspread. If file number entered is  there, then patient details of that specific file no is displayed to user before returning user to menu | as expected | 

## Manual testing of user choosing "b" in menu_choice()
|Choice | Input | Expected result | Response |
|---|---|---|---|
| Enter patient's name, surname, email, DOB, file no | Empty strings entered for patient name or surname | empty values are passed through not_empty function to return user to enter input again if string entered was empty.| as expected |
| Enter patient's name, surname, email, DOB, file no  | Email entered is invalid | Emails inputed are passed through validate_email() fxn to check if email written matches with valid email format. User is prompt to enter email again if invalid | as expected |
| Enter patient's name, surname, email, DOB, file no | Invalid DOB format | The date of Birth entered is passed through function validate_birthdate() to check if date entered is in the correct format first before checking if DOB is not a date in the future or present.If date entered is not in correct format, then error message "This is not a valid entry" is displayed to user| as expected | 
| Enter patient's name, surname, email, DOB, file no  | Date inputed is in the future or is the present day |The date of Birth entered is passed through function validate_birthdate() to check if DOB is not a date in the future or present.If date entered is in the future, then error message "This is not a valid birthdate, try again" is displayed to user  before requesting DOB again| as expected |
| Enter patient's name, surname, email, DOB, file no | File no inputed in wrong format | File no is passed through file_no_pattern() fxn to check correct format, if not then user is promt to enter file no again | as expected | 
| Enter patient's name, surname, email, DOB, file no | File no inputed already exists in patient's sheet | A valid file no is passed through validate_fileno() fxn to check file number entered is already present in Patient's sheet in gspread, if it is already present, then error message "This file no is already added" is displayed to user before returning user to main menu | as expected | 
| Enter patient's name, surname, email, DOB, file no | All inputs entered are valid | Name, surname, email, DOB and file number is first appeneded to a list and add_details method of class Patient is called.The method passes the new list as its argument , which allows the values in the list to be appended to a new row in Patients sheet in gspread.