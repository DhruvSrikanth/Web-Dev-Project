# Web Development Canvas Final Project

## Requirements:

- `sqlite3`
- `python3`

Once the above requirements are met, install the required `python` dependencies - 

```
pip3 install -r requirements.txt
```

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
## Run instructions (For running the server API):

```
python3 api.py
```
