﻿# nike-database

 ## Installation & Usage
1. Before running the program, please install 2 Python packages: prettytable and faker
```
pip install prettytable
```
```
pip install faker
```

2. Run main.py to use the program
```
py main.py
```

## Structure
* FinalPrj_DDL.sql: DDL file of the database
* queries.py: a class Query that includes a set of queries that the database admin can use when running the main program
* main.py: interface for all the user roles including customer, database admin, and guest. 

## Additional Notes
* For testing purposes, the admin account has username 'dbadmin' and password 'secret'. All information about user roles are saved in the users table in our database
 






