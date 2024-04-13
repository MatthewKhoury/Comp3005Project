# COMP3005 Project 2: Health and Fitness Club Management System

# Authors
  - Matthew Khoury, #101188452
  - Evan Baldwin, #101222276

# Description
This project models a Health and Fitness Club Management System utlizing a relational database
and Python scripts which form GUIs utilized to interface with and query the database. 
The database for this system is implemented in PostgreSQL utilizing the provided DDL and DML files
to create all tables necessary for implementation and populate those tables with data necessary to
demonstrate all functionalities. A demonstration of the conceptual design of the system, as well as 
critical code components and individual functionalities can be found at the following link:
https://youtu.be/3R8jK65Y3Ko

There are three individual applications run through the GUI scripts which each model a separate user
interface. The memberGUI and member files allow a club member to register a new account and manage their
profiles by altering personal information/goal/health metrics. Additionally, they can display a dashboard 
containing info such as exercise routines, fitness achievements, and health statistics. Members can 
schedule both personal training sessions or group fitness classes depending on the availability of both
the classes and the trainers. 

The trainerGUI and trainer files allow a fitness instructor to register for a new account, manage their
availability for personal sessions, and view individual member profiles. The adminGUI and admin files allow
an admistrator of the club to book rooms for classes, monitor equipment maintenance, update class schedules, 
and process existing bills created by members upon registering or joining classes. All of these functions are
performed by accepting user input and interfacing with the relational database to insert, update and retrieve 
information relevant to the query. 

# Using the program
- Execution:
  -Member: To run the program from the members perspective, you are first
   greeted with a login/registration window. this window is neccessary to
   allow members to only interact with their own personal information and
   not mess up other peoples information. Upon a succesful login the member
   will be greeted with a new window to access and manipulate their data base
   through a user friendly Graphical user interface.
   
  -Trainer:Running the code from the trainers side will follow a similar concept. 
   Each trainer will have the chance to log in and/or register to the database. 
   Upon a succesful login/registration the trainer will then be greeted with a 
   new window to which he again will then get the chance to manipulate their 
   database with their own functions.
   

  -Admin:From the Admin perspective there is only a log in feature as we believe
  for safttey of the data base no one should be allowed to register as an admin
  without proper screening. Upon a succesful log in the admin wil be granted access
  to modify room bookings, equipment maintenance and class scheduling. The admin
  should also be given access to view and accept payments through the application.
  These payments are dynamically added in when a user registers.

# Deliverables
- Source code:
  - Python scripts for each GUI and related functions can be found in 
    the folder labeled "COMP3005 Project".

- Conceptual ER Diagram:
  - Diagram representing the conceptual design of the database can be
    found in the folder labeled "diagrams" under the name of
    “COMP3005_Project_ER_Diagram”.

- Relational Schema:
  - Diagram representing the conceptual ER diagram reduced consolidated
    into tables can be found in the folder labeled "diagrams" under the
    name of “COMP3005_Project_Relation_Schema_Diagram”. 

- DDL File:
  - A .sql file containing statements necessary to construct the relational
    database can be found in the folder labeled "SQL" under the name of
    “COMP3005_Project_DDL”. 

- DML File:
  - A .sql file containing statements necessary to populate the relational
    dateabase can be found in the folder labeled "SQL" under the name of 
    “COMP3005_Project_DML”. 

- Final Report:
  - A pdf containing the project report with further elaboration on design
    decisions and implementation can be found under the name of 
    "COMP3005 Project2 Final Report".


	
	
# Bonus Features
- Additional features beyond the requirements outlined in the project specifications were implemented.
  Some examples of those additions include:
    - Ability for member to view all bills
    - Ability for admin to view all equipment
    - Ability for member to view all fitness goals
    - Ability to register new trainer with detailed information
