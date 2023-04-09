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