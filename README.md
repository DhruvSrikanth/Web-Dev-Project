# Web Development Canvas Final Project

In this repository, you will find the source code, database and instructions on how to run the created application. We have created a web-based application of the **Canvas** website.

## Technology Used:
- SQL
- Javascript
- HTML
- CSS
- Python
## Database Details:

We used `SQLite`, version 3 for this project. The schema for the database can be found in the `./database/create_db.sql` file.
## Backend Server API:

The backend was implemented using `Flask` API. This API utilizes the `REST` API and transmits `JSON` objects at the backend.
## Requirements:

- `sqlite3` (for the `database`)
- `python3` (for the `server API`)

Once the above requirements are met, install the required `python` dependencies - 

- flask
- datetime
- pytz
- re
- sqlite3

## Database Instructions (For running a new instance of the database):

1. Enter the correct directory - 
```
cd database
```

2. Create the database - 
```
sqlite3 database.db
```

3. Create the schema - 
```
.read create_db.sql
```

4. Populate the schema - 
```
.read populate_db.sql
```

5. Return - 
```
.exit
cd ..
```

## Account Setup (Initial):

After populating the database, you will need to login as an **admin** to activate other users (**student**, **teacher**). As an admin, you will be able to check the default inactive users provided in the **settings** page.

Admin Account - 
```
Username (Email ID) : admin1@uchicago.edu
Password : @password1
```

## Run instructions (For running the server API):

```
python3 api.py
```

## Accessing Website:

The website can be found at the following address:
```
http://localhost:8080/
```

The same can be found [here](http://localhost:8080/).

## Video Demonstration:

The video demonstration (walkthrough) on how to use the website, can be found [here](https://drive.google.com/drive/folders/16zL1ZzIMbvp6CpXDmkSKIUOIMvbfWlWp?usp=sharing). 


