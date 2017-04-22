# this file should contain all code to control roboBuoy
# it should consolidate code from all the modules in the
# roboBuoy_control_modules directory

# from roboBuoy_modules import VoltageMonitor, LeakDetection, GPS, Magnetometer, MotorControl


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
