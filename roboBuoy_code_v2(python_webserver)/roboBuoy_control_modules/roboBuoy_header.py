class GpsController(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
		self.running = False

	def run(self):
		self.running = True
		while self.running:
			# grab EACH set of gpsd info to clear the buffer
			self.gpsd.next()

	def stopController(self):
		self.running = False

	@property
	def fix(self):
		return self.gpsd.fix

	@property
	def utc(self):
		return self.gpsd.utc

	@property
	def satellites(self):
		return self.gpsd.satellites

	@property
	def satellitesUsed(self):
		set = self.gpsd.satellites
		if len(set) == 0:
			return 0
		count = 0
		for sat in set:
			if "Used: y" in str(sat):
				count = count + 1
		return count

# log following line after defining gps
# logger.info('GPS class defined.')

# Any code which should run when shutting down the program goes here.
# TODO: have this be called whenever the program stops, such as from control-C.
def motorStop():
	logger.warn("Stopping motor control!")
	# Not sure if this matters, but it seems safer to explicitly tell the
	# thrusters to stop before shutting down the control system.
	PWM.add_channel_pulse(dma, forward_thruster_pin, start, THRUST_OFF)
	PWM.add_channel_pulse(dma, turn_thruster_pin, start, TURN_OFF)
	servo.stop_servo(forward_thruster_pin)
	servo.stop_servo(turn_thruster_pin)
	PWM.clear_channel_gpio(0, forward_thruster_pin)
	PWM.clear_channel_gpio(0, turn_thruster_pin)
	PWM.cleanup()

def collectMagCalibration(mag):
	global mag_x_min, mag_x_max, mag_y_min, mag_y_max, mag_z_min, mag_z_max
	logMax = False
	if mx < mag_x_min:
		mag_x_min = mx
		logMax = True
	if my < mag_y_min:
		mag_y_min = my
		logMax = True
	if mz < mag_z_min:
		mag_z_min = mz
		logMax = True
	if mx > mag_x_max:
		mag_x_max = mx
		logMax = True
	if my > mag_y_max:
		mag_y_max = my
		logMax = True
	if mz > mag_z_max:
		mag_z_max = mz
		logMax = True
	if logMax:
		logger.debug("raw mx,y,z ranges " + str(mag_x_min) + " " + str(mag_x_max)
					   + "  " + str(mag_y_min) + " " + str(mag_y_max)
					   + "  " + str(mag_z_min) + " " + str(mag_z_max))


# Use the magnetometer to compute magnetic heading and then return
# true heading in degrees between 0 and 360.
def getTrueHeadingTiltComp(lsm):
	global MX_MIN, MX_MAX, MY_MIN, MY_MAX, MZ_MIN, MZ_MAX
	global logNow
	# Read from the sensor and pull out values.
	accel, mag = lsm.read()


	# Use accelerometer values to get pitch and roll
	ax, ay, az = accel
	# x is pitch, negative = bow up
	# y is pitch, positive = tilt to port
	# z must be vertical, reads about 1000 when level
	# Normalize
	aNorm = math.sqrt(ax*ax + ay*ay + az*az)
	ax = ax / aNorm
	ay = ay / aNorm
	# Positive pitch is normally defined as nose up, and positive roll is to starboard
	# We work in radians for these angles
	pitch = math.asin(-ax)
	roll = math.asin(-ay/math.cos(pitch))
	# if logNow: logger.debug("Pitch, roll: " + str(int(180*pitch/math.pi)) + ", " + str(int(180*roll/math.pi)))

	# Use magnetometer values to get uncompensated field strengths
	mx, my, mz = mag

	# Record min/max magnetometer values.  Turn on after installing a new
	# magnetometer or changing its magnetic "neighborhood".
	if COLLECT_MAG_CALIBRATION_RANGE:
		collectMagCalibration(mag)

	# Values must be offset - probably different for each copy of the breakout.
	# Scale to +-1
	mx = 2.0*(mx - MX_MIN)/(MX_MAX - MX_MIN) - 1.0
	my = 2.0*(my - MY_MIN)/(MY_MAX - MY_MIN) - 1.0
	mz = 2.0*(mz - MZ_MIN)/(MZ_MAX - MZ_MIN) - 1.0

	# Using a new strategy compared to the original getMagneticHeading, convert
	# the x, y, z system we have to that which typical code expects.  Then we
	# can use outside code examples without translation.
	# Originally we found that atan2(mz, mx) gave good headings after adding 180.
	# Most code uses atan2(my, mx)
	# That means that our z becomes y, our x stays x and our y becomes z (or minus z??)
	# BUT this gives a result 180 degrees off.  To rotate axes by 180, x and z both change signs.
	myTemp = my
	my = -mz
	mz = myTemp
	mx = -mx

	# Keep the commented logger line below for checking magnetometer calibration, especially
	# after installing a new one.  If there are multiple RoboBuoys we will probably want a single
	# version of the code to read a local copy of a file which has the offsets for  the
	# specific RoboBuoy it lives on.
	# logger.debug("raw mx ranges " + str(mag_x_min) + " to " + str(mag_x_max) + " for mz: " + str(mag_z_min) + " to " + str(mag_z_max))
	# logger.debug("mxyz: " + str(mx) + ", " + str(my) + ", " + str(mz) )

	# the m?Comp variables are compensated for pitch and roll (tilt)
	# Note the minus sign on the pitch values.  This is experimentally determined, and
	# is NOT what the reference show.  e.g.
	# http://blog.solutions-cubed.com/lsm303-compass-tilt-compensation/
	# https://www.sparkfun.com/datasheets/Sensors/Magneto/Tilt%20Compensated%20Compass.pdf
	mxComp = mx * math.cos(-pitch) + mz * math.sin(-pitch)
	myComp = mx * math.sin(roll) * math.sin(-pitch) + my * math.cos(roll) - mz * math.sin(roll) * math.cos(-pitch)
	# mxComp is not actually compensated. We don't use mzComp, but we print all three.
	mzComp = mz
	# compute a heading in degrees
	heading = 180 * math.atan2(myComp, mxComp) / math.pi
	# correct for declination
	heading = heading + declination
	# be sure we didn't go past 360, and to be safe check for negatives.
	while heading > 360:
		heading = heading - 360
	while heading < 0:
		heading = heading + 360
	# if logNow:
	# 	logger.debug("compensated mxyz: " + str(round(mxComp,4)) + ", " + str(round(myComp,4)) + ", " + str(round(mzComp,4)) + ", " + str(int(heading)) )

	return heading
