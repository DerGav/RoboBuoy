# this file contains all the code to define roboBuoy's webserver's behavior

# import functions from libraries so we can use them
#   - 'flask' lets our python script act like a webserver
#     we don't need everything so just import a few things from flask
from flask import Flask,render_template,jsonify, request

# import our target destination management file to get the destinations
# 'as' keyword allows us to give it a shorter (arbitrary) name
import roboBuoy_targetDestination_management as targets

# initialize Flask webapp
app = Flask(__name__)

# define global variables used for testing during development
i = 0
received_data = []

# for a request to the root directory of our webpage call the index() function
@app.route('/')
# define a function (fka Subroutine) called index
def index():
    # render (=translate) the file 'index.html' from the templates directory to
    # real html and return it to the browser that requested it
    return render_template('index.html')

#define what to do for request to '/some_value'
@app.route('/some_value')
def add_numbers():
    # we need to add this line so we can use the global variable i in this function
    # python would otherwise create a new local variable with the same name
    global i
    # create 'dictionary' and fill it with data pairs (key and value)
    # filled with bogus values right now for testing
    # eventually should be filled with data from RoboBuoy
    data = {
                '2. someValue1': i,
                '1. someValue2': '&#8594; East', # '&#8594;' = code for arrow
                '3. xand another one': 300

            }

    # increment the global(!) variable i to simulate a changing value for testing
    i += 1;

    # This line sends the data to whoever requested it, most likely some browser.
    # Because browsers generally don't speak python the function 'jsonify'
    # takes the python dictionary 'data' and translates it to
    # JavaScriptObjectNotation(JSON) so that it can be processed by a browser.
    return jsonify(data)

# this route doesn't serve a page or data but instead
# receives data from the browser, hence methods=['POST']
@app.route('/receive_command', methods=['POST'])
def receiveCommand():
    # for now lets store the received data in a global variable
    global received_data

    # the request object contains the data the browser sent to the server
    # because we took it from a form object it is stored at request.form
    received_data = request.form

    # send a message to the browser saying that everything went ok
    # TODO: maybe some sort of validation of the data should be added here
    return jsonify({'status':'OK'})

# this route is just there for development purposes right now
# it simply sends the data the server received back to the browser Because
# it is easier to view it there
@app.route('/show_received')
def show_received():
    # specify that received_data refers to global variable received_data
    global received_data
    return jsonify(received_data)

@app.route('/send_targetDestinations')
def send_targetDestinations():
    return jsonify(targets.get_target_destinations())
