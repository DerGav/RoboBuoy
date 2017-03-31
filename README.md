# Synopsis
This repository contains the control software code for CSUMB's RoboBuoy.
*  **v1** contains the code as it was submitted by the Spring 2016 MSCI 437/410 class
*  **v2** is a work in progress attempt at redesigning the control software

# roboBuoy_code_v1
For an explanation of this version of the code refer to the technical manual.
Note that this repo only contains the code files, for information on where to place these files on RoboBuoy to run the code also refer to the techincal manual.
# roboBuoy_code_v2
This is a work in progress attempt of redesigning and simplifying the code.

* **roboBuoy_python_webserver_test.py** currently contains only the code to run a flask webserver on roboBuoys Raspberry Pi
In future this file could be merged with roboBuoys main motor control script, to eliminate the need of the motor control    script communicating with the server and instead have it serving the control page or at least the data to be displayed directly
* the **templates** directory contains html templates to be rendered by the python webserver
  * **index.html** defines the basic layout of the main control page viewed on the tablet. It also loads and runs the 'roboBuoy.js' file on the client
* the **static** directory contains javascript and css files 
  * **roboBuoy.js** is the main javascript file for the control page (index.html) it handles the communication between the control page and the python webserver
  * **roboBuoy_styles.css** changes the apperance of the control page
  * the jQuery files are libraries containing prewritten javascript and css to make the page look nice
  
## Installation
v2 is not ready to be used on RoboBuoy yet. It can however be run on a computer for development:
1. install python and flask 
2. Download or clone the repository and navigate to the v2 directory
3. run **roboBuoy_python_webserver_test.py** using python 
4. open a browser at http://127.0.0.1:5000 to view the control page
   * If you want to view the control page on a different device (e.g. smartphone, tablet) open a browser there and go to http://<your_computers_ip_adress>:5000.