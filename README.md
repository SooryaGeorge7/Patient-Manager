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

## Logic and Features

### Python flowchart 

A flowchart was created in the start of the project to help build logic for the system.
![Patient Manager Flow Diagram](documentation/flow-chart/flow-chart.png)

### DataSheet

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
