'''
	this is the main roboBuoy code file which should be run on startup
	it manages the two threads and uses all the other code files
'''
# import module which allows us to create and run threads
import threading
# import our webserver file so we can run the server from here
from roboBuoy_webserver import create_app
# import our RoboBuoy control class
from roboBuoy_control   import RoboBuoy

# create an instance of our RoboBuoy class
roboBuoy = RoboBuoy()

# create flask app and pass the RoboBuoy instance
app = create_app(roboBuoy)

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
	# infinite loop as a placeholder for the roboBuoy code
	while True:
	   pass


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
	# main thread is exited
	# the main thread here is essentially this main function which doesn't do
	# anything apart from starting the other threads
	# NOTE: this setup may not be desirable in production, but is useful during
	# development, as it allows the whole program to be started and stopped from
	# the terminal
	t.setDaemon(True)
	# append thread to the array
	threads.append(t)
	# and start it
	t.start()

	# connect the roboBuoy function to a thread
	t = threading.Thread(target=roboBuoyControl)
	# make this thread a 'daemon' too
	t.setDaemon(True)
	# append it to the array
	threads.append(t)
	# and start the thread
	t.start()

	# try the following code block and handle an exception if there is one...
	try:
		# Join all threads using a timeout so it doesn't block
		# Filter out threads which have been joined or are None
		# "joining" threads means that the executing thread (main thread), will
		# wait for the specified other thread (t) to exit before resuming
		threads = [t.join(1000) for t in threads if t is not None and t.isAlive()]
	# handle a KeyboardInterrupt (Ctrl-C from the terminal)
	except KeyboardInterrupt:
		# print sth to show that this line is actually being executing
		print "main Exit"



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
