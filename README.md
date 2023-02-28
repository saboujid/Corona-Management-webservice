# README for Corona Archive

### Contributors  
  
- Aboujid Saad
- Chigozirim Margaret Arukwe
- Blen Assefa
- Alina Amanbayeva
- Aghakhan Huseynli
- Flavia Tasellari

# Sprint 1   

## About the Project
The purpose of this document is to build a web service for Corona disease management which enables digital tracking of citizens which enter certain places and keeping the records in case of a Covid infection spread.

### Built with
* HTML
* CSS
* [Python3](https://www.python.org/download/releases/3.0/)
* [Bootstrap](https://getbootstrap.com/docs/5.0/getting-started/download/)
* [Flask](https://www.fullstackpython.com/flask.html)
* [SQLite](https://www.sqlite.org/index.html)

## File Structure
```
\--SE-Sprint01-Team15

        \--static
            \--css                  # All the CSS Files used
            \--img                  # All the images used 
            \--js                   # Some js files
        \--templates    
            \--                     # Main HTML files    
        \--database  
            \--                     # .db files for sorting the databases
        \--tests
            |--test_base.py        # Main Testing Python Code
        -- app.py                   # Main Python Code
        -- database.py              # Main Database connection code
        -- config.py                # Global variable(Password) for creating a session
        -- README.md
        -- requirements.txt         # Required flask dependencies to run this program
        -- .gitignore    
```

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. What things you need to install the software and how to install them.V
### Prerequisites

* Sqlite3
* Flask 
```
pip3 install Flask
```
* Virtual Env
```
sudo pip3 install virtualenv 
```

## Installation Guide

```bash
# Clone the repo.
$ git clone https://github.com/Magrawal17/SE-Sprint01-Team15.git

# go inside the directory
cd SE-Sprint01-Team15/

# Create virtual environment
$ virtualenv env

# Start virtual environment
$ source env/bin/activate

# Install all the dependencies
$ pip3 install -r requirements.txt

# Run python server
$ python3 app.py

```

# View Documentation

Go to this URL once the server has started.

```
http://localhost:5000/docs
```
# Run tests

Run this code once you are entire the environment

```sh
$ python3 tests/test_base.py
```

### Sample Data

An Agent with the following username and password already exisits in the database. Since only and agent
is allowed to create another, it made sense to create an agent initially.
<br>
Username - Agent <br>
Password - 12345 <br>
## Properties
The properties object must define the following attributes:
### Agent

| Property | Type | Description | Example |
| ------ | ------ | ------ | ------ |
| ```agent_id``` | Int | An identifier for the Agent in the database. | ```"agent_id":1234``` |
| ```username``` | String | An identifier for the user as an agent, that they can use to login. | ```"username":"Agent 1"``` |
| ```Password``` | String | Password used for login in | ```"Password":"ABC123"``` |


### Visitor

| Property | Type | Description | Example |
| ------ | ------ | ------ | ------ |
| ```citizen_id``` | Int | An identifier for the Visitor in the database. | ```"citizen_id":1234``` |
| ```username``` | String | An identifier for the user as Visitor, that they can use to login. | ```"username":"ABC123"``` |
| ```Password``` | String | Password used for login in | ```"Password":"ABC123"``` |
| ```visitor_name``` | String | A property of the visitor. | ```"visitor_name":"ABC123"``` |
| ```address``` | String | Address of visitor | ```"address":"Hot St."``` |
| ```phone_number``` | String | Contact Information of the visitor. | ```"phone_number":"+491234567890"``` |
| ```email``` | String | Contact Information of the visitor | ```"email":"ABC123@gmail.com"``` |
| ```device_id``` | String | An identifier for the device a user is trying to use for entering a place. | ```"device_id":"ABC123"``` |
| ```infected``` | Bool | A ```True``` or ```False``` value for the infection status of a visitor. | ```"infected":True``` |

### Hospital

| Property | Type | Description | Example |
| ------ | ------ | ------ | ------ |
| ```hospital_id``` | Int | An identifier for the Hospital in the database. | ```"hospital_id":1234``` |
| ```username``` | String | An identifier for the user as a Hospital, that they can use to login. | ```"username":"Mr. Doctor Strange"``` |
| ```Password``` | String | Password used for login in | ```"Password":"ABC123"``` |
| ```status``` | Int | Valus from ```0``` to ```2```.  ```0``` - Waiting for Approval or Rejection. ```1``` -  Approved. ```2``` -  Rejected.| ```"status":1``` |


### Place

| Property | Type | Description | Example |
| ------ | ------ | ------ | ------ |
| ```place_id``` | Int | An identifier for the Place in the database. | ```"place_id":123``` |
| ```username``` | String | An identifier for the user as a Place, that they can use to login. | ```"username":"The owner"``` |
| ```Password``` | String | Password used for login in | ```"Password":"ABC123"``` |
| ```place_name``` | Int | Name of the certain place that wants it's visitors recorded. | ```"place_name":"My Cafe"``` |
| ```address``` | String | An identifier for the place to register. | ```"address":"Hot Street"``` |
| ```qrcode``` | String | A unique key for a visitor to use for creating a new ```VisitsToPlace``` object. | ```"qrcode":"ABC123"``` |


### VisitsToPlace

| Property | Type | Description | Example |
| ------ | ------ | ------ | ------ |
| ```vtp_id``` | Int | An identifier visit to a certain place. | ```"vtp_id":123``` |
| ```place_id``` | String | An identifier for the place a visitor is trying to visit. | ```"place_id":"ABC123"``` |
| ```device_id``` | String | An identifier for the user of the system. | ```"device_id":"ABC123"``` |
| ```entry_time``` | Date | Date value that contains the time as well. | ```"entry_time":"ABC123"``` |
| ```exit_time``` | Date | Date value that contains the time as well. | ```"exit_time":"ABC123"``` |

# Sprint 2 Changes

## Installation
You can follow the steps [here](https://flask.palletsprojects.com/en/2.0.x/installation/) to create a virtual environment in our application's working directory. 
### Start the virtual environment.
### for mac and linux
    
    source env/bin/activate

### for windows

    env\Scripts\activate 

### Run the server

    export FLASK_APP=run.py
    flask run

Then, open http://127.0.0.1:5000/ in your web browser to view our application.

! You might also need to change the port in run.py (the last line of code) 


## Changes
- Registration redirects to corresponding login page
- Added all fields required for signup for all user types
- Hospitals can be verified
- Hospitals can mark visitors as infected
- Hospitals can mark visitors as not infected
- Webcam implemented

## Bug Fixes
- "Place register not working" bug fixed
- "Already have an account? Login here" invalid link fixed
- Hospital verified status shows after re login in Admin dashboard
- Visitor infected/uninfected status shows after re login in Hospital dashboard
- Sometimes even after installing flask-mail, the message sent by the user will not be recieved!!

## Fixes required
- Make get device id a server sided function
- Convert the qrcode to a pdf and download the pdf
- Provide your email and password in config.py file, in order to recieve the sended mails from the user, otherwise those will be sent to the previous group's memeber email!
- Install flask-mail extension -

      pip3 install Flask-Mail

# Sprint 3

# Installation: 

Clone the repository 
```
git clone https://github.com/Magrawal17/se-03-team-15.git
```
Go into the directory
```
cd se-03-team-15
```
Install
```
pip3 install flask
```
```
pip3 install virtualenv
```
```
pip3 install Flask-Mail
```
Create the Virtual Environment
```
virtualenv env (OR TRY python -m virtualenv env)
```
Start the Virtual Environment
```
source env/bin/activate (FOR WINDOWS env\Scripts\activate)
```
Install the required library
```
pip3 install -r requirements.txt
```
Run the app
```
export FLASK_APP=run.py
flask run

FOR WINDOWS
set FLASK_APP=run.py
flask run
```
Then copy the provided url into any browser

## Run tests

python .\tests\test_base.py

## Sample Data

An Agent with the following username and password already exists in the database. 
<br>
Username - Agent<br>
Password - 12345<br> 

Visitor, Place and Hospital with these username and password exist in database.
<br>
Username - admin<br>
Password - admin<br>


# Documentation of Progress in Sprint 3

- Web Cam API has been implemented in Visitor Dashboard.

- Visitors are able to scan the QR code.

- Sign up now invalid link has now been fixed in the all login pages.

- Device ID has now been passed as a hidden field (following the specification in the design).

- Created again the table VisitorToPlace in the database following the specifications in the design.

- Created the You're in page in Visitor portal.

- Set entry time and exit time.

- Time that the visitor stays in a place is shown in the You're in page.

- Created a Leave button for the visitor to leave the place and be able to scan again.

- Created form validation.

- Created sessions after the logins (this way a certain user cannot access other pages of the other users)

- Web Cam has been connected to the database. 

- The connection between the visitor and the place is stored in the database.

- Tables of Visitors and Places have been added to Agent dashboard.

- Created search pages and new forms in the agent page (functionality to be added in the next sprint).

- Generally UI has been improved (some texts were invisible before, added new photo).

- Added new testcases and fixed some of the previous tests.

- Verification of Hospitals in Agent dashboard is shown instantly. (Before we had to re-login to see the changes)

- Infection status of visitors in Hospital dashboard is shown instantly. (Before we had to re-login to see the changes)

# Sprint 4

# Installation: 

Clone the repository 
```
git clone https://github.com/Magrawal17/se-04-team-15.git
```
Go into the directory
```
cd se-04-team-15
```
Install
```
pip3 install virtualenv
```

Create the Virtual Environment
```
virtualenv env (OR TRY python3 -m virtualenv env)
```
Start the Virtual Environment
```
source env/bin/activate (FOR WINDOWS env\Scripts\activate)
```
Install the dependencies for the project
```
pip3 install -r requirements.txt
```
Run the app
```
export FLASK_APP=run.py
flask run
(or just: python3 run.py)

FOR WINDOWS
set FLASK_APP=run.py
flask run
```
Then copy the provided url into any browser

## Sample Data

An Agent with the following username and password already exists in the database. 
<br>
Username - Agent<br>
Password - 12345<br> 

Visitor, Place and Hospital with these username and password exist in database.
<br>
Username - admin<br>
Password - admin<br>


## Documentation of Progress Sprint 4

- Modified text in the homepage into meaningful information instead of random text.   

- Fixed footer which was previously covering pages' content.  

- Changed fonts to poppins to improve readability.

- Fixed logo to always appear while navigating the app; it previously appeared only on homepage (also fixed the broken link).

- Modified and changed the coloring for more synergy . 

- Fixed the *about us* page and added imprint instead of some random text.

- Added functionality for agents to search for visits to a place within a time interval. Only a form previously existed with no functionality.

- Provided functionality for agents to search for a visitor's visiting history within a time period.

- Created new html files to display these information.

- Created new routes in *run.py* for the same purpose.

- Regulated access to these routes using session variables(only logged in agents have access to the functionalities).

- Edited *search_visit_byvisitor.html* to include the right route for posting data (Same for *search_visit_toplace.html*).

- Provided test script to test created routes (session variables were also tested in the process).

## **Run test**
```python3 tests/test_sprint4.py```


