# this file should contain all code to control roboBuoy
# it should consolidate code from all the modules in the
# roboBuoy_control_modules directory

# from roboBuoy_modules import VoltageMonitor, LeakDetection, GPS, Magnetometer, MotorControl

i = 0

class RoboBuoy(object):
	"""docstring for RoboBuoy."""
	def __init__(self):
		super(RoboBuoy, self).__init__()

	def startup(self):
		print("enabling opto coupler")

	def setup(self):
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
			# #voltageCheck(pin, slope, intercept)
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
			# # self.mag_heading = getTrueHeadingTiltComp(lsm) #current heading - in degrees
			# # self.current_lat = self.gpsc.fix.latitude
			# # self.current_long = self.gpsc.fix.longitude
			# # self.sats_used = str(self.gpsc.satellitesUsed)
			#
			# ############################################################################
			# # calculate distance
			# ############################################################################
			#
			# # calc the midpoint of latitude
			# latMid = (self.current_lat + self.target_lat) / 2.0
			# m_per_deg_lat = 111132.954 - 559.822 * math.cos(2.0 * latMid) + 1.175 * math.cos(4.0 * latMid)
			# m_per_deg_long = m_per_deg_lat * math.cos(latMid)
			#
			# # Gives +/- when appropriate to know where it's heading
			# deltaLatToTar  = self.target_lat - self.current_lat
			# deltaLongToTar = self.target_long - self.current_long
			# self.distance_to_target = math.sqrt(math.pow(deltaLatToTar * m_per_deg_lat, 2) + math.pow(deltaLongToTar * m_per_deg_long, 2))
			#
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
			# degrees_bearing = theta * 180.0 / math.pi
			# turn_angle = degrees_bearing - mag_heading
			#
			# # In case we end up outside the range of +/- 180 degrees:
			# while (turn_angle > 180.0):
			# 		turn_angle = turn_angle - 360.0
			# while (turn_angle < -180.0):
			# 		turn_angle = turn_angle + 360.0
			#
			#
			# ############################################################################
			# # Move forward thruster
			# ############################################################################
			#
			# if distance_to_target > TARGET_IS_FAR:
			# 	#PWM.add_channel_pulse(dma, forward_thruster_pin, start, THRUST_STRONG)
			# 	MotorControl.thrust_strong()
			# elif distance_to_target <= TARGET_IS_FAR and distance_to_target > TARGET_IS_CLOSE:
			# 	#PWM.add_channel_pulse(dma, forward_thruster_pin, start, THRUST_SOFT)
			# 	MotorControl.thrust_soft()
			# elif distance_to_target <= TARGET_IS_CLOSE:
			# 	# stop?
			# 	#PWM.add_channel_pulse(dma, forward_thruster_pin, start, THRUST_OFF)
			# 	MotorControl.thrust_stop()
			#
			# ########################################################################
			# # Move turn thruster
			# ########################################################################
			#
			# # first, a little logic so we are less likely to oscillate between hard-left and hard-right
			# # when faced almost straight away from the target.
			# # do the old and new angles have opposite sign?
			# if math.copysign(1, last_turn_angle) != math.copysign(1, turn_angle):
			# 	# are they both large?
			# 	if (math.fabs(last_turn_angle) + overlap_at_180 > 180) and (math.fabs(turn_angle) + overlap_at_180 > 180):
			# 		# are they within overlap_at_180?
			# 		if 180-math.fabs(last_turn_angle)+180-math.fabs(turn_angle) < overlap_at_180:
			# 			# ignore the computed angle and just use the last one.  Eventually either
			# 			# we'll turn so that actual computed values can be used or we'll
			# 			# get beyond the overlap range and switch to turning the other way.
			# 			turn_angle = last_turn_angle
			# last_turn_angle = turn_angle
			#
			# # 4/5/16: don't turn if you are within 2 m (TARGET_IS_CLOSE) - both because the angle
			# # probably can't be trusted and so the LEDs turn off.
			# if (distance_to_target <= TARGET_IS_CLOSE) or (turn_angle < turn_threshold and turn_angle > -turn_threshold):
			# 	# close enough, don't turn
			# 	turn_direction = '--'
			# 	MotorControl.turn_stop()
			# elif turn_angle >= turn_threshold:
			# 	# turn right
			# 	turn_direction = '&rarr;' + repr(math.trunc(math.fabs(turn_angle)))
			# 	MotorControl.turn_right()
			# elif turn_angle <= -turn_threshold:
			# 	# turn left
			# 	turn_direction = '&larr;' + repr(math.trunc(math.fabs(turn_angle)))
			# 	MotorControl.turn_leftt()

		return

	def handleCommand(self, message):
		# for now just print the command
		print(message['command'])



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

	def stop(self):
		print("send stop signal to motors")
		print("write new destinations to file")
		self.run = False
