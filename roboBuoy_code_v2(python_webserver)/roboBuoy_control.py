# this file should contain all code to control roboBuoy
# it should consolidate code from all the modules in the
# roboBuoy_control_modules directory

#from roboBuoy_modules import VoltageMonitor, LeakDetection, GPS, Magnetometer, MotorControl
import math
#i = 0

class RoboBuoy(object):
	"""docstring for RoboBuoy."""
	def __init__(self):
		super(RoboBuoy, self).__init__()
		#self.voltageMonitor = VoltageMonitor(22)


	def startup(self):
		print("enabling opto coupler")

	def setup(self):
		#setup voltage monitoring

		# LeakDetection.setup()

		# start gps
		# self.gpsc = GPS.GpsController()
		# self.gpsc.start()
		#logger.info("GPS controller started.")

		# TODO: do this here? or just call the read function from file?
		# The magnetometer!
		#self.lsm = Adafruit_LSM303.LSM303()
		#logger.info("Magnetometer started.")
		#print ("Magnetometer started.")

		# setup motors
		#MotorControl.setup()
		self.run = True
		pass

	def start(self):
		while self.run:
			pass
			# ############################################################################
			# # leak detection
			# ############################################################################
			#
			# #if(LeakDetection.checkForLeak()):
			# # TODO:handle leak
			# 	#warning to page
			# 	#shutdown motors?
			# 	#stop control script?
			# ############################################################################
			# # battery voltage check
			# ############################################################################
			#
			#self.battery_voltage = voltageCheck(VoltageMonitor.batteryPin, VoltageMonitor.slope, VoltageMonitor.intercept)
			# #TODO:handle voltage
			# 	#warning to page
			# 	#shutdown motors?
			# 	#shutdown pi?
			#
			# ############################################################################
			# # Read Sensor data
			# ############################################################################
			#
			# # Get all the sensor data we'll be using for navigation:
			# self.mag_heading = Magnetometer.getTrueHeadingTiltComp(lsm) #current heading - in degrees
			# self.current_lat = self.gpsc.fix.latitude
			# self.current_long = self.gpsc.fix.longitude
			# self.sats_used = str(self.gpsc.satellitesUsed)
			#
			# ############################################################################
			# # calculate distance
			# ############################################################################
			#
			# # calc the midpoint of latitude
			# latMid = (self.current_lat + self.target_lat) / 2.0
			# m_per_deg_lat = 111132.954 - 559.822 * math.cos(2.0 * latMid) + 1.175 * math.cos(4.0 * latMid)
			# m_per_deg_long = m_per_deg_lat * math.cos(latMid)

			# Gives +/- when appropriate to know where it's heading
			# deltaLatToTar  = self.target_lat - self.current_lat
			# deltaLongToTar = self.target_long - self.current_long
			# self.distance_to_target = math.sqrt(math.pow(deltaLatToTar * m_per_deg_lat, 2) + math.pow(deltaLongToTar * m_per_deg_long, 2))

			# ############################################################################
			# # Calculate current bearing to target from lat and long.
			# ############################################################################
			#
			# # Thinking out loud for the inputs to atan2:
			# # deltaLatToTar is positive if we are south of the target.
			# # deltaLongToTar is positive if we are west of the target.
			# # However, if we give atan2 the usual arguments of (y,x) it will calculate the angle
			# # counterclockwise from east, just like the unit circle in trig class.
			# # We need to go clockwise from north.  It turns out that swapping north and east (lat and long) fixes that.
			# theta  = math.atan2(deltaLongToTar, deltaLatToTar)
			#
			# # Convert bearing to degrees
			# # Note that mag_heading already includes +13 declination adjustment
			degrees_bearing = theta * 180.0 / math.pi
			turn_angle = degrees_bearing - mag_heading

			# In case we end up outside the range of +/- 180 degrees:
			while (turn_angle > 180.0):
					turn_angle = turn_angle - 360.0
			while (turn_angle < -180.0):
					turn_angle = turn_angle + 360.0
			#
			if(self.move_thrusters):
				pass
				#move thrusters here
		return
	def handleCommand(self, message):
		# for now just print the command
		print(message['command'])

		if  message['command'] == "start_stop_roboBuoy":
			pass
		elif message['command'] == "start_stop_thrusters":
			if message['value'] == "running":
				self.move_thrusters = true
			elif message['value'] == "stopped":
				self.move_thrusters = false
			pass
		elif message['command'] == "shutdown":
			pass
		elif message['command'] == "set_new_target":
			pass
		elif message['command'] == "save_targets":
			pass


	def getData(self):
		# print sth so we now we're actually in this function
		print("getting data...")
		# create 'dictionary' and fill it with data pairs (key and value)
		# data = {
		# 			'current_lat' : self.current_lat,
		# 			'current_long': self.current_long,
		# 			'target_lat' : self.target_lat,
		# 			'target_long': self.target_long,
		# 			'sats_used' : self.sats_used,
		# 			'mag_heading' : self.mag_heading,
		# 			'distance_to_target' : self.distance_to_target,
		# 			'speed': self.speed,
		# 			'turn_direction': self.turn_direction,
		# 			'leak' : False,
		# 			'battery_voltage': self.battery_voltage
		# 		}
		data = {
					'current_lat' : 36.1234,
					'current_long': -121.1234,
					'target_lat' : 36.4321,
					'target_long': -121.4321,
					'satellites_used' : 7,
					'mag_heading' : 23,
					'distance_to_target' : 402,
					'speed': "Fast",
					'turn_direction': "left",
					'leak' : True,
					'battery_voltage': 15.2
				}


		return data;

	def stop(self):
		print("send stop signal to motors")
		print("write new destinations to file")
		self.run = False
