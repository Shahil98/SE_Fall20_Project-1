# About Flask App




## approach



## Code Description

1. ```Flask_App/flask_server.py``` implements the main server. 
2. ```Flask_App/templates/index.html``` represents the home page the user will enter.
3. ```Flask_App/templates/base.html``` provide the template web format for every html page.

### flask_server.py  

This file basically sets up the REST API for our remote server. Users can interact with the server via this RESTful API. At the backend, this code contains functions to query the database and display the stats and graphs for each user. Different functions inside are:  

1. ```index()``` method render the main page (index.html).
2. ```login()``` method is called when user click "login" in the main page. It will call the '''form.py''' to create a form. When user click submit, it will take the input(userID)
and call method '''dashboard()''' 
3. ```dashboard()``` method is called whenever client sends his/her userID from method ```login()```. This method takes ```uid``` as input, then 
query the database using two function(```retrieve_data_table_chart()``` and ```retrieve_data_pie_chart()``` ) in the ```sql_actions.py```. Once we get the user's information(e.g. File Name, Time spend for each file), we plot pie chart and table chart to analysis user's time spend on each file or project and render ```dashboard.html```.
4. ```signup()``` This function generates a unique ID for each user, and adds it to the database.
5. ```send()```This function waits for the HTTP GET request from the user and adds the necessary information regarding each file for a user into the database.

### form.py
create a form for login, in this case we just need uid, Datarequired means we do not accept empty string as input and the length should be 1-200  
 
### sql_actions.py  
This file contains all the necessary functions to run SQL queries on the server database. Different functions inside are:  
1. ```add_data_users()``` take the userID as input, insert this userID into Users table in our database.
2. ```add_data_dashboard()``` take the user's usage data as input, insert this information into Dashboard talbe in our database. This function is called whenever the sublime plugin makes a HTTP POST request to the REST API with the details regarding the user and his’/her’s files.  
3. ```retrieve_data_table_chart()``` take userID as input, query the database the retrieve data from database and send back to method ```dashboard()``` to plot table chart.
4. ```retrieve_data_pie_chart()``` take userID as input, query the database the retrieve data from database and send back to method ```dashboard()``` to plot pie chart.

### create_db.py  
This file creates the database that is needed to store the details regarding each user of the software. It uses MySQL and python integration to create the DB tables. Different functions inside are:  

```_drop_tables(db)```This drops the already present tables inside the DB if any.  
```create_tables(db)```This contains the code to create and design the tables.  

### base.html

1. provide nav-bar template apply to every page in our application.
2. provide content format apply to every page in our application.
3. provide page title(Codetime) apply to every page in our application.

### index.html

1. ```login link```
2. ```home link```


### dashboard.html
This html file is rendered using the ```dashboard()``` function to display the statistics.

