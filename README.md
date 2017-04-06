# Synopsis
This repository contains the control software code for CSUMB's RoboBuoy.
*  **v1** contains the code as it was submitted by the Spring 2016 MSCI 437/410 class
*  **v2** is a work in progress attempt at redesigning the control software

# roboBuoy_code_v1
For an explanation of this version of the code refer to the technical manual.
Note that this repo only contains the code files, for information on where to place these files on RoboBuoy to run the code also refer to the techincal manual.

**Update** : **motor_control_3_03-28-2017.py** is a new version of the v1 code, containing a few minor changes and more comments to clarify the files structure

# roboBuoy_code_v2
This is a work in progress attempt of redesigning and simplifying the code.

* **roboBuoy.py** is the code file that should be executed to run this new roboBuoy control software. It doesn't do that much itself, but it executes code from the other files, serving as a sort of 'commandcentral'
* **roboBuoy_webserver.py** currently contains the code to run a flask webserver on roboBuoys Raspberry Pi
* **roboBuoy_control.py** should in future be the main script to read from the sensors, calculate the distance and control roboBuoy's thrusters. To do so it should execute code from the files located in the **roboBuoy_modules** folder
* **roboBuoy_modules** contains some files, which each contain the code to 'operate' one of roboBuoy's components. The code is splitted out into several files in an attempt to make the whole project more organized
* the **templates** directory contains html templates to be rendered by the python webserver
  * **index.html** defines the basic layout of the main control page viewed on the tablet. It also loads and runs the 'roboBuoy.js' file on the client
* the **static** directory contains javascript and css files 
  * **roboBuoy.js** is the main javascript file for the control page (index.html) it handles the communication between the control page and the python webserver. It also defines all the user interactions, e.g. what happens when a button is clicked etc.
  * **roboBuoy_styles.css** changes the apperance of the control page
  * the jQuery files are libraries containing prewritten javascript and css to make the page look nice
  
## Installation
v2 is not ready to be used on RoboBuoy yet. It can however be run on a computer for development:
1. install python and flask 
2. Download or clone the repository and navigate to the v2 directory
3. run **roboBuoy.py** using python (on a Mac or Linux just open a console, navigate to that directory and type "python roboBuoy.py"
4. open a browser at http://127.0.0.1:5000 to view the control page
   * If you want to view the control page on a different device (e.g. smartphone, tablet) open a browser there and go to http://<your_computers_ip_adress>:5000. You may be asked in a dialog if you want to allow python to accept incoming network connections. Allow this if you want to view the page from a device other than your computer
