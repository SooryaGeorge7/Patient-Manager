# Dental Patient Manager

## Brief 

This python project is specifically developed for a dental or medical private practice. 

This is a simple patient management system that would allow users(eg. admin) to add, view or edit  appointments, treatments and patient details. 

I decided to build this project for my 3rd portfolio project for code instutute having drawn inspiration from my current work life. 

I decided to challenge myself with a trying to complete a command line python application that would allow me to manage patients similarly to the applications used in real dental private practices. 

## Table of contents
  - [Brief](#brief)
  - [User Stories](#user-stories)
    - [First time visitor](#first-time-visitor)
    - [Returning visitors](#returning-visitors)
  - [Logic and Features](#logic-and-features)
    - [Python](#python)
    - [Database](#database)
    - [Features](#features)
  - [Future implementation](#features-left-to-implement)
  - [Technologies Used](#technology-used)
    - [Languages Used](langues-used)
    - [Frameworks, Libraries and Programs Used](#frameworks,-libraries-and-programs-used)
  - [Testing](#testing)
  - [Bugs](#bugs)
    - [Solved Bugs](#solved-bugs)
    - [Known Bugs](#known-bugs)
  - [Deployment](#deployment)
    - [Deployment to Heroku](#deployment-to-heroku)
    - [How To Fork](#how-to-fork)
    - [How To Clone](#how-to-clone)
  - [Credits and Acknowledgements](#credits-and-acknowledgements)
    - [Code Used](#code-used)
    - [Content](#content)
    - [Media](#media)
    - [Acknowledgements](#acknowledgements)


## User Stories 

### First time visitor
* I want to be able to sign in to the program.
* I want to view patient's details 
* I want to add appointments for a patient.
* I want to edit or view treatments. 
* I want to find the price of treatments.

### Returning visitor
* I want to be able to log in succesfully. 
* I dont want to sign up again. 

# Logic and Features

## Python flowchart 

A flowchart was created in the start of the project to help build logic for the system.
![Patient Manager Flow Diagram](documentation/flow-chart/flow-chart.png)

## DataSheet

Google Sheets were used to store data from user into spread sheet and to export data when neccessary as well.
This project has a total of 4 worksheets. 

1. The users sheet 

![Users sheet](documentation/datasheets/users-sheet.png)

The users sheet contains the user's username and password(hashed with bcrypt). The hashed password is stored in case if the system
is hacked they would not be able to access passwords to log in to the program.
This sheet is user when patient tries signing in/registering to store new username/password and when loging in to check if inputed username and password match the ones in the datasheet.

2. The patients sheet

![Patients sheet](documentation/datasheets/patients-sheet.png)

The patients sheet contains the patient details of patients. Namely their first name, surname, email address, birthdate and file number.
This sheet is used when viewing patient details and when adding patient details.It is also used to access patient's name when viewing appointments.

3. The appointments sheet

![Appointments sheet](documentation/datasheets/appointments-sheet.png)

The appointments sheet contains patient file no, appointment date, time, treatment and price.
This sheet is used when adding appointments and viewing appointments. All values in the sheet are entered by user except for the values in the price column.The prices in price column is imported from treatments sheet when user enter's patient's treatment for that appointment.

4. The treatments sheet

![Treatments sheet](documentation/datasheets/treatments-sheet.png)

The treatments sheet contains all treatments offered in the dental clinic and the prices for each.
This sheet is accessed when viewing prices,adding treatment prices to show total payment due and to check for treatment prices when adding appointment for a patient. 

## Features

*  MAIN PAGE

![Main Page](documentation/features/main-page.png)

Main page/ Start screen consists of ASCII logo, welcome message with short description and a menu to choose between log in or sign up.

![Main Page Error](documentation/features/main-page-error.png)

If you dont enter a valid option( a or b), then program will give error message and then will let user choose again.

--- 

* LOG IN

![Log in Feature](documentation/features/login-process.png)

Once you choose (a) , The user is allowed to enter username and password.

![Log in Error](documentation/features/login-error.png)

User should only log in if they have already signed up/ registered.If the system does'nt have your username or password in datasheet, it will display this error message and will allow you to choose to sign up or log in again.

---

* REGISTER/SIGN UP

![Sign in Feature](documentation/features/signin-process.png)

Once you choose to sign up or register, you will be allowed to enter a new username. If the same username is already stored in data sheet users, user will be given an error message and asked to enter another user name. Once validated, proceeds to ask for  a new password and then to confirm that password.

![Sign in succesfull](documentation/features/signup-succesfull.png)

Once you have signed in, program allows you to log in.

![Empty string error](documentation/features/empty-string-error.png)

For any string that the system has to store such as new password, new username, first name(needed to add patient details) and surname (needed to add patient details). The program then makes sure that user does not enter an empty string for those inputs.

![Passwords error](documentation/features/passwords-error.png)

When asked to confirm password, if passwords dont match then user is displayed an error message before asking to start again.

---

* MAIN MENU

![Main Menu](documentation/features/main-menu.png)

One user logs in successfully, The main menu is displayed which has 5 options(a - e) to choose from.

![Main menu error](documentation/features/main-menu-error.png)

If user doesnt choose an option from (a -b ), then user is displayed an error message before asking to choose again.

* MENU OPTION A

![View patient feature](documentation/features/menu-option-a/view-patient-option.png)

If user chooses option "a", Program asks user to enter a file number(unique code for each patient). 

![File no pattern error](documentation/features/menu-option-a/file-no-pattern-error.png)

The file number has a specific unque pattern, if user doesnt enter a file number with the correct pattern/format, it will give off this error. This error is shown everytime user doesnt enter a file number in the correct pattern at any time the user is required to enter a file number in the program. 

![File no error](documentation/features/menu-option-a/no-file-num.png)

If you enter a file number in the correct pattern/format, but we dont have this patient's details in the patients sheet , then user is given error message and will return user back to main page inorder for them to add the patient details of that specific file number.

![Patient Details](documentation/features/menu-option-a/view-patient-details.png)

If user does enter a valid file number and it is stored in Patient's sheet in gspread, The program exports/ returns the patient's details connected to that specific file number.The user then is returned back to the main menu to be able to choose an option again.

* MENU OPTION B 

![Add patients process](documentation/features/menu-option-b/add-patient-details.png)

To add patients, user is asked to enter patient's name, surname, birthday, email and file number.
If added succesfully, user is returned to the main menu.

![Date format error](documentation/features/menu-option-b/date-format-error.png)

The date entered by user should be in the correct formula, otherwise it will give an error before asking to enter enter date again.

![Birthday error](documentation/features/menu-option-b/birthday-error.png)

The date entered in the correct formula should be a date in the past, if not then an error message will be displayed before user is aasked to enter birthdate again.

![Email error](documentation/features/menu-option-b/email-error.png)

The email entered is validated, if its not in the format of an email. Program will display error message before asking to enter an email again. 

As for the names , user gets displayed an error message if they enter an empty string before requesting to enter the name or surname. The file number should also be given in the correct format/pattern in order to be validated. 

* MENU OPTION C

![Appointment options](documentation/features/menu-option-c/appointment-options.png)

The menu option "c" displayed another menu for user to choose. a - To add appointment, or b - to view appointments. 

![choice error message](documentation/features/menu-option-c/option-c-error.png)

If user chooses neither a or b, an error message is displayed before asking user to choose again.

 * ADD APPOINTMENT 

 ![Adding pt process](documentation/features/menu-option-c/add-appointment/adding-appointments.png)

 If user chooses "a",then program proceeds to ask user for patient's file no, appointment date , time and treatment.

 ![Add pt details error](documentation/features/menu-option-c/add-appointment/add-patientdetails-error.png)

 If user enters a file number that is not in the patients sheet in gspread, then user is returned to main menu to add patient's details first.This ensure that patient's details needs to be in the database before you can add an appointment for that patient.

 ![Unavailable date error](documentation/features/menu-option-c/add-appointment/unavailable-appointment.png)

 If user enters a date and time which is already been entered/used in appointment sheet in gspread, then an error message is shown before return user to menu.This ensures that the user cant book more than 1 patient for a specific date and time .


 ![Appointment date error](documentation/features/menu-option-c/add-appointment/appointment-date-error.png)

 If user enters a date in the past, this error message will be shown before they are asked to enter appointment date again

 The time entered should also be written in the correct format or pattern , if not an error is displayed before allowing user to enter time again.

 ![Added message](documentation/features/menu-option-c/add-appointment/added-successfully.png)

 If appointment is added succesfully, a messaged is displayed before returning user to the main menu

 * VIEW APPOINTMENT

 ![View appointment](documentation/features/menu-option-c/view-appointment/view-appointment.png)

 When user chooses option b- to view appointment, user is prompt to enter patient's file number. The file number is used to retrieve patient's name and surname from patients sheet. The file number is also used to retrieve the appointment details of the patient in the appointment sheets. All appointments made for this particular patient is displayed to user with treatment cost as well.

 ![View Appointment error](documentation/features/menu-option-c/view-appointment/view-appointment-error.png)

 If user enter's a file number that is not in the appointments sheet, the user is displayed an error message to add appointment first. 

* MENU OPTION D

![Treatment options](documentation/features/menu-option-d/menu-d-options.png)

When user chooses menu option d- treatments, program displays another option to user that allows user to calculate total payment due or to view prices.
 
 * PAYMENT DUE 

 ![Treatment options](documentation/features/menu-option-d/payment-due/treatment-options.png)

 When user chooses option a - total payment due, the is asked to choose from the treatment options shown. 

 ![Treatment option error](documentation/features/menu-option-d/payment-due/treatment-option-error.png)

 If user doesnt choose one of the treatment options from the list( doesnt matter if they enter in UPPERCASE or LOWERCASE), an error message is displayed before asking user to enter treatment option again. 

 ![After choice options](documentation/features/menu-option-d/payment-due/after-treatmentoption.png)

 After user enters a valid treatment option , user is displayed another message which allows them to choose between adding another treatment option or viewing total payment due.
 If user chooses - add another treatment option, then user is displayed the treatment options to choose again.

 ![Total due](documentation/features/menu-option-d/payment-due/total-due.png)

Once user chooses total payment due, then the user is displayed the total cost of all the treatments you have added previously.

 * TREATMENT PRICES

 ![Treatment prices](documentation/features/menu-option-d/prices/treatment-prices.png)

 If user chose to view treatment prices, a list of treatments with their respective prices are shown to the user . These values are exported from the treatments sheet.

* MENU OPTION E
 
 If user chooses menu option "e", the system allows you to return to start screen of the program.

---

## Future implementation 
* I want to add css styling to be able to mimick a real life application.  
* Id want to give user more options such as adding and calculating treatments for each patient. 
* An option to say if patient has paid for treatments or not.
* An option to add notes for each patient.
* Add much more details for patients information( taking in address etc)

## Technologies Used

### Languages Used

* Python is predominently used, with the project template having javascript and html as well. 
### Frameworks, Libraries and Programs Used

* [GitHub](https://github.com/)- To save and store files
* [Gitpod](https://gitpod.io/workspaces)- Code editor
* [Git](https://git-scm.com/) - For Version control
* [Heroku](https://heroku.com) - For deployment
* [Google sheets API](https://developers.google.com/sheets/api) - To store and fetch data
* [Diagrams.net](https://diagram.net) - Used to make flowchart 
* [CI Python Linter](https://pep8ci.herokuapp.com/) - To validate code
* [Ascii Art](https://www.asciiart.eu/) - For start of game art piece 
## Testing

## Bugs 
### Solved Bugs
### Known Bugs

## Deployment 

### Deployment to Heroku

The site was deployed to heroku with the following steps: 

1. Type in pip3 freeze > requirements.txt in terminal to add to requirements.txt
2. Git add, git commit and push changes.
3. Visit [Heroku](https://id.heroku.com/login) to creat an acount. 
4. Click on "Create new app".
5. I entered my app name as "patient-manager-system"
6. Enter region as Europe.
7. Click on Create App Button.
8. The new page contains several tabs. Select settings tab first. 
9. Scroll down in settings tab to Section "Config Vars"
10. Click button "Reveal Config Vars"
11. Go back to gitpod and copy creds.json contents
12. In the KEY field under Config Vars ,Enter "CREDS" (NB:UPPERCASE)
13. In the VAlue field under COnfid Vards, paste contents of creds.json.
14. Click button "Add"
15. Add another KEY - "PORT"
16. Add another VALUE - "8000"
17. Click button "Add" again.
18. Scroll down to "Build Packs" section, and click on "Add Build Pack"
19. In the pop up window, click on "Python" and then "Save Changes"
20. click on "Add Build Pack" again and click on "node.js" and then "Save Changes" again
21. The buildpacks should be in the order of "Python" on top, and "node.js" underneath.
22. Scroll up, and then click on the "Deploy" Tab.
23. Scroll down and go to section "Deployment Method", select "Git Hub"
24. Confirm that you want to connect to Github below .
25. Once connected, Type in the name of repository ( This project - Patient-Manager) and click on "Search"
26. Once the "Patient-Manager" repository is found, click on connect.
27. Once connected, scroll down to automatic deploy. Click on "Enable Automatic Deploys"
28. Afterwards, click on "Deploy Branch" . 
29. Once you see the message "the app was succesfully deployed", then the app link will be provided to you.
29. You can click on that to view deployed heroku terminal.
30. I added Coloroma, and Bcrypt after deploying which needed to be added to requirements.txt using pip3 freeze > requirements.txt in order for them to operate on the deployed heroku terminal.

### How To Fork

To fork the Patient-Manager Repository:

Log in or Sign up to github.
Find the repository for this project, SooryaGeorge7/Patient-Manager
Click the fork button on top right corner.
How to Clone

### How To Clone

To clone the Patient-Manager Repository:

Log in or Sign up to github.
Find the repository for this project, SooryaGeorge7/Patient-Manager.
Click on Code button just left to the green gitpod button.
Select what you would like to clone with (HTTPS/SSH/GitHub CLI) and copy the link shown below.
Open the terminal in your code editor(eg. Gitpod) and change the current working directory to the location you want to use for cloned directory.
In the terminal type in "git clone" and paste the link you copied in step 4 above. Press enter.
Cloning is now completed.

## Credits and Acknowledgements

### Code Used
### Content 
### Media
### Acknowledgements
