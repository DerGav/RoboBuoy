# this file should contain all code to control roboBuoy
# it should consolidate code from all the modules in the
# roboBuoy_control_modules directory

# from roboBuoy_modules import VoltageMonitor, LeakDetection, GPS, Magnetometer, MotorControl

i = 0

class RoboBuoy(object):
	"""docstring for RoboBuoy."""
	def __init__(self):
		super(RoboBuoy, self).__init__()

	def __setup(self):
		# setup voltage monitoring

		# LeakDetection.setup()

		# start gps
		#self.gpsc = GPS.GpsController()
		#self.gpsc.start()
		#logger.info("GPS controller started.")

		# TODO: do this here? or just call the read function from file?
		# The magnetometer!
		#lsm = Adafruit_LSM303.LSM303()
		#logger.info("Magnetometer started.")
		#print ("Magnetometer started.")

		# setup motors
		#MotorControl.setup()
		pass
	def handleCommand(self, command):
		# for now just print the command
		print(command)

		# TODO: add code to handle commands here

	def getData(self):
		# print sth so we now we're actually in this function
		print("getting data...")

		# we need to add this line so we can use the global variable i here
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

		return data;
