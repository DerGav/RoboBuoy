# this is the main roboBuoy code file which should be run on startup
# it manages the two threads and uses all the other code files

import threading # this allows us to create and run threads
# import our webserver file so we can run the server from here
import roboBuoy_webserver
from roboBuoy_control import RoboBuoy

# get the Flask app from our webserver file and store it in a variable
app = roboBuoy_webserver.app

roboBuoy = RoboBuoy()

# this function simply runs the server
def runServer():
    # run the flask webapp we initialized at the top
    #  "debug=True" :
    #       run in debug mode (a bit slower, but easier to troubleshoot)
    #  "use_reloader=False" :
    #       diasble reloader so the server can run in a thread
    #       means that script has to be restarted for changes to take effect
    #  "host='0.0.0.0'" :
    #       runs the server on the pi's IP-Adress and so makes it
    #       available to anyone in the same network
    app.run(debug=True, use_reloader=False, host='0.0.0.0')
    # app.run(debug=True)
    # app.run(debug=False, host='0.0.0.0')

# this function should contain roboBuoy control code in future
def roboBuoyControl():

    while True:
       print('doing stuff...')


# create array to hold threads
threads = []

# this is pythons way of saying:"start code execution here" ('main' function)
# detailed explanation:
#   http://ibiblio.org/g2swap/byteofpython/read/module-name.html
if __name__ == '__main__':

	# we want the webserver and the roboBuoy control code to run concurrently
	# if you have parts of code that should be executed at the same time
	# instead of writing 2 seperate programs you can write 1 program with
	# multiple 'threads'
	# that way it is a lot easier for those threads to share information
	# but they still run (pseudo) concurrently
	# we will start a 'thread' for the webserver
	# and another for the roboBuoy control code

	# connect the server function to a thread
	t = threading.Thread(target=runServer)

	# make this thread a 'daemon'
	# this essentially means that it will be automatically stopped once the
	# main roboBuoy thread is exited
	# NOTE: this may not be desirable in production, but is useful during
	# development, as it allows the whole program to be started and stopped from
	# the terminal
	t.setDaemon(True)

	# append thread to the array
	threads.append(t)
	# and start it
	t.start()

	# connect the roboBuoy function to a thread
	t = threading.Thread(target=roboBuoyControl)
	# append it to the array
	threads.append(t)
	# and start the thread
	t.start()

	# Uncomment following code instead of the threads if you just want to
	# run a single thread with the server. That may be easier for development.

	# run the flask webapp we initialized at the top
	#  "debug=True" :
	#       run in debug mode (a bit slower, but easier to troubleshoot)
	#  "host='0.0.0.0'" :
	#       runs the server on the pi's IP-Adress and so makes it
	#       available to anyone in the same network
	# app.run(debug=True, host='0.0.0.0')
	# app.run(debug=True)
