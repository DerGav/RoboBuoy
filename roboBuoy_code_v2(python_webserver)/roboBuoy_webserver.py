# this file contains all the code to define roboBuoy's webserver's behavior

# import functions from libraries so we can use them
#   - 'flask' lets our python script act like a webserver
#     we don't need everything so just import a few things from flask
from flask import current_app, Blueprint, Flask,render_template,jsonify, request

# import our target destination management file to get the destinations
# 'as' keyword allows us to give it a shorter (arbitrary) name
import roboBuoy_targetDestination_management as targets

# define a flask blueprint (a blueprint for a webserver app) and call it control
# also tell it where to find the templates and static directories
control = Blueprint('control', __name__,
					template_folder='templates',
					static_folder='static')

# define 'application factory' - function that creates a flask app
def create_app(roboBuoy_instance):
	# create flask app
	app = Flask(__name__)
	# tell it to use our control blueprint
	app.register_blueprint(control)
	# pass roboBuoy instance to the flask app
	app.config['ROBOBUOY'] = roboBuoy_instance
	# return our new and configured flask app
	return app


# define global variables used for testing during development
i = 0
received_data = []

# for a request to the root directory of our webpage call the index() function
@control.route('/')
# define a function (fka Subroutine) called index
def index():
	# render (=translate) the file 'index.html' from the templates directory to
	# real html and return it to the browser that requested it
	return render_template('index.html')

#define what to do for request to '/some_value'
@control.route('/some_value')
def add_numbers():
	# # we need to add this line so we can use the global variable i in this function
	# # python would otherwise create a new local variable with the same name
	# global i
	# # create 'dictionary' and fill it with data pairs (key and value)
	# # filled with bogus values right now for testing
	# # eventually should be filled with data from RoboBuoy
	# data = {
	# 			'2. someValue1': i,
	# 			'1. someValue2': '&#8594; East', # '&#8594;' = code for arrow
	# 			'3. xand another one': 300
	#
	# 		}
	#
	# # increment the global(!) variable i to simulate a changing value for testing
	# i += 1;

	# request data from RoboBuoy class
	data = current_app.config['ROBOBUOY'].getData();

	# This line sends the data to whoever requested it, most likely some browser.
	# Because browsers generally don't speak python the function 'jsonify'
	# takes the python dictionary 'data' and translates it to
	# JavaScriptObjectNotation(JSON) so that it can be processed by a browser.
	return jsonify(data)

# this route doesn't serve a page or data but instead
# receives data from the browser, hence methods=['POST']
@control.route('/receive_command', methods=['POST'])
def receiveCommand():
	# for now lets store the received data in a global variable
	global received_data

	# the request object contains the data the browser sent to the server
	# because we took it from a form object it is stored at request.form
	received_data = request.form

	# call roboBuoy's handle command function
	# to access it use the config attribute of the flask app that is using this
	# blueprint and that has called this function
	current_app.config['ROBOBUOY'].handleCommand(received_data)

	# send a message to the browser saying that everything went ok
	# TODO: maybe some sort of validation of the data should be added here
	return jsonify({'status':'OK'})

# this route is just there for development purposes right now
# it simply sends the data the server received back to the browser Because
# it is easier to view it there
@control.route('/show_received')
def show_received():
	# specify that received_data refers to global variable received_data
	global received_data
	return jsonify(received_data)

@control.route('/send_targetDestinations')
def send_targetDestinations():
	return jsonify(targets.get_target_destinations())
