## Code Description

1. ```code/SublimePlugin/codeTime.py``` defines functions to permorm actions when a window is activated, deactivated or closed in sublime text editor and 
also starts periodic log saving function. 
2. ```code/SublimePlugin/periodicLogSaver.py``` defines a class PeriodicLogSaver which has functions which are used to periodically send data to the server.

### codeTime.py

This file implements following functions:
1. ```when_activated()``` method is called by the ```on_activated()``` method to log the start timestamp of the activate window.
2. ```when_deactivated()``` method is called by the ```on_deactivated()``` method to log the end timestamp of the deactivated window.
3. ```CustomEventListener.on_activated()``` method is invoked when a window becomes active and it calls the ```when_activated()``` method to log the start timestamp.
4. ```CustomEventListener.on_deactivated()``` method is invoked when a window deactivates and it calls the ```when_deactivated()``` method to log the end timestamp.
5. ```CustomEventListener.on_close()``` method is invoked when a window is closed and is used to send the data to server for the file whose window is closed.
6. ```plugin_loaded()``` method is invoked whenever the text editor is opened and it starts periodic log saving by calling the ```start()``` function of the PeriodicLogSaver class.

### periodicLogSaver.py

This file implements the following functions:
1. ```PeriodicLogSaver.__inti__()``` is a constructor for PeriodicLogSaver class which is especially used to initialize the object with data from the codeTime.py file.
2. ```PeriodicLogSaver.run()``` method is run periodically and calls the ```PeriodicLogSaver.write_log_file()``` function to send the data to the server.
3. ```PeriodicLogSaver.run()``` method is used to send the data to the server.
