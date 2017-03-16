# Brute force motor code for RoboBuoy Prototype
# Created by Cole Drake, John Freutel, Steve Ryan, Jorge Chagoya
# Last Change: 4-26-2016
# GPS code to be accredited to Martin O'Hanlon
# Magnetometer code to be accredited to Adafruit, adapted by Jorge Chagoya
# Lat/Long coords are converted into a distance to target in meters

#####################################################################
# Comments - add more for new programmers (new to this program or to Pi).
# Use "#QXYZ" for comments from Ximena Yeomans Zzxyz.
# - these comments should be checked for accuracy.
# 
##########################################

print "Initializing."

from RPIO import PWM
import RPIO
import time
import logging
from gps import *
import threading
import math
from lib.Adafruit_I2C import Adafruit_I2C
import Adafruit_LSM303
import os.path
import sys


# This variable was originally there to slow down output for readability.  Now we
# have logTimeInterval which can separately control the output rate of most logging.
# Critical logging should be immediate (not controlled by logTimeInterval).
MAIN_LOOP_DELAY = 0.1
logTimeInterval = 15  # seconds
# How many main loops between log outputs.  Change the lines above, not this one.
LOG_MULTIPLE = int(logTimeInterval / MAIN_LOOP_DELAY)
# Counter variable for logging.
logNow = True
recentEpxy = 0.0


#
# ONLY USED WITHOUT THRUSTERS
#
import RPi.GPIO as GPIO
POWER_LED = 24
LEFT_LED = 25
RIGHT_LED = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(POWER_LED, GPIO.OUT)
GPIO.setup(RIGHT_LED, GPIO.OUT)
GPIO.setup(LEFT_LED, GPIO.OUT)
#
#

#Checking and removing stop.txt so the program can run
if os.path.isfile("/home/pi/data_to_buoy/stop.txt") == True:
	os.remove("/home/pi/data_to_buoy/stop.txt")
if os.path.isfile("/home/pi/data_to_buoy/leak.txt") == True:
	os.remove("/home/pi/data_to_buoy/leak.txt")

turn_threshold = 10.0
# If we are turning (say) 178 degrees right and the next calculation says 178 degrees left
# we could just start oscillating back and forth.  Allow this many degrees past 180 before
# changing the sign.
overlap_at_180 = 10.0
last_turn_angle = 0.0

forward_thruster_pin = 17
turn_thruster_pin = 18
target_lat = 36.62388
target_long = -121.90735

dma = 0
start = 10

# Magnetometer corrections
# 13.3 is a good declination for Marina, CA in 2016.  Change when traveling.
declination = 13.3

# Diagnostics to see the range of mx, mz values
# When a new magnetometer is installed, diagnostics should be turned on and
# then robobuoy should be turned  and rotated in all directions (including upside
# down) until new min/max values are not found (logging of those lines will stop).
# Then the values must be copied into the MX_MIN and other values in the next
# section.
COLLECT_MAG_CALIBRATION_RANGE = False
mag_x_min =  1000
mag_y_min =  1000
mag_z_min =  1000
mag_x_max = -1000
mag_y_max = -1000
mag_z_max = -1000

# The ranges from the diagnostics are recorded here, and used to scale mx, my, mz
# to both center and scale the ranges.
# Note that the ".0" after each value is not a significant figure, but it may
# help ensure that later code does floating point math rather than integer rounding.
MX_MIN = -443.0
MX_MAX =  636.0
MY_MIN = -649.0
MY_MAX =  370.0
MZ_MIN = -669.0
MZ_MAX =  447.0

TARGET_IS_FAR = 10  # meters
TARGET_IS_CLOSE = 2 # meters

# Thrust magnitude control
THRUST_OFF = 150
THRUST_SOFT = 160
THRUST_STRONG = 175
# Turn power
TURN_RIGHT = 145 
TURN_LEFT = 155
TURN_OFF = 150

# Set up logging.
# We will use the following definitions of the built-in loggin levels.
# - debug: more detail than a user would ever want, but useful to the programmer
# - info: possibly useful to a user, but not indicating a problem
# - warning: something which should not happen, but doesn't break functionality
# - error: for events which will lead to seriously incorrect behavior
# - critical: physical damage to the buoy or complete failure is expected
# The logger:
logger = logging.getLogger('RoboBuoy')
logger.setLevel(logging.DEBUG)
# Log to a file, usually with high detail:
log_fh = logging.FileHandler('robobuoy.log')
log_fh.setLevel(logging.DEBUG)
# Log to the console, with less detail:
log_ch = logging.StreamHandler()
log_ch.setLevel(logging.INFO)
# Define message format - not sure if there's a default:
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_fh.setFormatter(formatter)
log_ch.setFormatter(formatter)
# handlers must be added to the logger
logger.addHandler(log_fh)
logger.addHandler(log_ch)


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

logger.info('GPS class defined.')

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

gpsc = GpsController()
gpsc.start()
logger.info("GPS controller started.")
RPIO.setup(4, RPIO.IN) #pin 4 will be an I/O input pin - leak detection circuit
logger.info( "Setting up PWM and DMA.")
PWM.setup()
PWM.set_loglevel(PWM.LOG_LEVEL_ERRORS)
PWM.init_channel(dma)
# Set initial speed to zero
speed = "Start at Zero"
turn_direction = "Start at Zero"
PWM.add_channel_pulse(dma, forward_thruster_pin, start, THRUST_OFF)
time.sleep(1)
PWM.add_channel_pulse(dma, turn_thruster_pin, start, TURN_OFF)
time.sleep(1)
logger.info("Done setting up PWM and DMA")

# The magnetometer!
lsm = Adafruit_LSM303.LSM303()
logger.info("Magnetometer started.")

servo = PWM.Servo()
logger.info("servo started.")

time.sleep(1)
print "Starting in 3..."
time.sleep(1)
print "2..."
time.sleep(1)
print "Starting to move."
logger.info('Starting motor control')
time.sleep(1)

logCount = 0
while os.path.isfile('/home/pi/data_to_buoy/stop.txt') or os.path.isfile('/home/pi/data_from_buoy/leak.txt') == False:
	# Log only avery LOG_MULTIPLE passes
	logCount = logCount + 1
	logNow =  logCount >= LOG_MULTIPLE
	if logNow:
		logCount = 0
	leak_input = RPIO.input(4)
	if leak_input == False:
		#shuts down the thrusters and sends leak alert to contol pad
		leak_alert = open('/home/pi/data_from_buoy/leak.txt', 'w')
		leak_alert.close()
		motorStop()

	try:
		emergency_file = open('/home/pi/data_to_buoy/battery.txt')
	except IOError:
		logger.error("No battery status file.  Is the monitor running?")
		motorStop()
		sys.exit(0)
		logger.error("did we really exit?")
	check_emergency = emergency_file.readlines()
	if logNow:
		logger.debug(check_emergency)
	em = "EM"
	if em in check_emergency[0]:
		# shut down everything
		logger.critical("STOPPING")
		motorStop()
		os.system("sudo halt")
	if em in check_emergency[1]:
		#shuts down just the thrusters
		logger.critical("SERVO SHUTDOWN")
		motorStop()
	
	# Get all the sensor data we'll be using for navigation:
	mag_heading = getTrueHeadingTiltComp(lsm) #current heading - in degrees
	current_lat = gpsc.fix.latitude
	current_long = gpsc.fix.longitude
	sats_used = str(gpsc.satellitesUsed)
	if logNow:
		logger.debug("Long error (m): " + str(gpsc.fix.epx))
		logger.debug("Lat  error (m): " + str(gpsc.fix.epy))
		recentEpxy = math.sqrt(gpsc.fix.epx*gpsc.fix.epx + gpsc.fix.epy*gpsc.fix.epy)
		logger.debug("Satellites used: " + sats_used + " position error " + str(round(recentEpxy, 1)))
	
	# Checking for files for either stopping or new coordinates
	while os.path.isfile('/home/pi/data_to_buoy/set_home.txt') == True: #checks for set_home to set it's current position as the new target position
		target_lat = gpsc.fix.latitude
		target_long = gpsc.fix.longitude
		logger.info("New home at current location: " + str(target_lat) + ", " + str(target_long))
		os.remove('/home/pi/data_to_buoy/set_home.txt') #removes the file
	while os.path.isfile('/home/pi/data_to_buoy/target_location.txt') == True: #checks for a new_coords file for a new target position
		# Reads all lines in the file
		infile = open('/home/pi/data_to_buoy/target_location.txt')
		coords_lines = infile.readlines()
		# Iterate through the list, one at a time until no more lines
		line_number = 0
		while line_number < len(coords_lines):
			target_lat = float(coords_lines[line_number])
			target_long = float(coords_lines[line_number+1])
			line_number += 2
		logger.info("New home from web page: " + str(target_lat) + ", " + str(target_long))
		os.remove('/home/pi/data_to_buoy/target_location.txt')

	if logNow:
		logger.debug("current_lat  and target_lat  = " + str(current_lat) + ", " + str(target_lat))
		logger.debug("current_long and target_long = " + str(current_long) + ", " + str(target_long))
		logger.debug("mag_heading  =  " + str(mag_heading))

	# Calculating distance to target
	latMid = (current_lat + target_lat) / 2.0  # calc the midpoint of latitude
	m_per_deg_lat = 111132.954 - 559.822 * math.cos(2.0 * latMid) + 1.175 * math.cos(4.0 * latMid)
	m_per_deg_long = m_per_deg_lat * math.cos(latMid)
	deltaLatToTar = target_lat - current_lat # Gives +/- when appropriate to know where it's heading
	deltaLongToTar = target_long - current_long # Gives +/- when appropriate to know where it's heading
	distance_to_target = math.sqrt(math.pow(deltaLatToTar * m_per_deg_lat, 2) + math.pow(deltaLongToTar * m_per_deg_long, 2))

	if logNow:
		logger.info("Distance to target = " + str(distance_to_target))

	# Calculate current bearing to target from lat and long. 
	# Bearing - 0 deg = N, 90 deg = E, 180 = S, 270 = W

	# Thinking out loud for the inputs to atan2:
	# deltaLatToTar is positive if we are south of the target.
	# deltaLongToTar is positive if we are west of the target.
	# However, if we give atan2 the usual arguments of (y,x) it will calculate the angle
	# counterclockwise from east, just like the unit circle in trig class.
	# We need to go clockwise from north.  It turns out that swapping north and east (lat and long) fixes that.

	theta  = math.atan2(deltaLongToTar, deltaLatToTar)

	# mag_heading is already in degreees.  Convert bearing as well.
	# Note that mag_heading already includes +13 declination adjustment
	degrees_bearing = theta * 180.0 / math.pi
	turn_angle = degrees_bearing - mag_heading
	# In case we end up outside the range of +/- 180 degrees:
	while (turn_angle > 180.0):
            turn_angle = turn_angle - 360.0
	while (turn_angle < -180.0):
            turn_angle = turn_angle + 360.0

	if logNow:
		logger.info("degrees bearing to target " + str(round(degrees_bearing, 1)))
		logger.info("magnetic heading " + str(round(mag_heading, 0)))
		logger.info("degrees to turn " + str(round(turn_angle, 0)))
		logger.info("distance to target " + str(round(distance_to_target, 1)))
        time.sleep(MAIN_LOOP_DELAY)

	if os.path.isfile('/home/pi/data_to_buoy/stop.txt') == False:
		# Speed control - everything is in meters at the "if" statements
		dist_text = ' (' + repr(round(distance_to_target, 1)) + ' m away)'
		if distance_to_target > TARGET_IS_FAR:
			speed = 'Going fast' + dist_text
			PWM.add_channel_pulse(dma, forward_thruster_pin, start, THRUST_STRONG)
			GPIO.output(POWER_LED, GPIO.HIGH)
		elif distance_to_target <= TARGET_IS_FAR and distance_to_target > TARGET_IS_CLOSE:
			speed = 'Approaching target' + dist_text
			PWM.add_channel_pulse(dma, forward_thruster_pin, start, THRUST_SOFT)
			GPIO.output(POWER_LED, GPIO.HIGH)
		elif distance_to_target <= TARGET_IS_CLOSE:
			speed = 'Close to target' + dist_text
			# stop?
			PWM.add_channel_pulse(dma, forward_thruster_pin, start, THRUST_OFF)
			GPIO.output(POWER_LED, GPIO.LOW)

		# Heading Control

		# first, a little logic so we are less likely to oscillate between hard-left and hard-right
		# when faced almost straight away from the target.
		# do the old and new angles have opposite sign?
		if math.copysign(1, last_turn_angle) != math.copysign(1, turn_angle):
			# are they both large?
			if (math.fabs(last_turn_angle) + overlap_at_180 > 180) and (math.fabs(turn_angle) + overlap_at_180 > 180):
				# are they within overlap_at_180?
				if 180-math.fabs(last_turn_angle)+180-math.fabs(turn_angle) < overlap_at_180:
					# ignore the computed angle and just use the last one.  Eventually either
					# we'll turn so that actual computed values can be used or we'll
					# get beyond the overlap range and switch to turning the other way.
					turn_angle = last_turn_angle
		last_turn_angle = turn_angle

		# 4/5/16: don't turn if you are within 2 m (TARGET_IS_CLOSE) - both because the angle
		# probably can't be trusted and so the LEDs turn off.
		if (distance_to_target <= TARGET_IS_CLOSE) or (turn_angle < turn_threshold and turn_angle > -turn_threshold):
			# close enough, don't turn
			turn_direction = '--'
			PWM.add_channel_pulse(dma, turn_thruster_pin, start, TURN_OFF)
			GPIO.output(LEFT_LED, GPIO.LOW)
			GPIO.output(RIGHT_LED, GPIO.LOW)
		elif turn_angle >= turn_threshold:
			# turn right
			turn_direction = '<font size=\"5\">&rarr;</font> ' + repr(math.trunc(math.fabs(turn_angle)))
			PWM.add_channel_pulse(dma, turn_thruster_pin, start, TURN_RIGHT)
			GPIO.output(RIGHT_LED, GPIO.HIGH)
			GPIO.output(LEFT_LED, GPIO.LOW)
		elif turn_angle <= -turn_threshold:
			# turn left
			turn_direction = '<font size=\"5\">&larr;</font> ' + repr(math.trunc(math.fabs(turn_angle)))
			PWM.add_channel_pulse(dma, turn_thruster_pin, start, TURN_LEFT)
			GPIO.output(RIGHT_LED, GPIO.LOW)
			GPIO.output(LEFT_LED, GPIO.HIGH)

	        #Writing key information about Robobuoy so it can be viewed via the webserver
		buoy_info = open('/home/pi/data_from_buoy/colecode.txt', 'w')
		buoy_info.write('<td>Turn Direction</td> <td>' + turn_direction + ' </td> \n' 
			+ '<td>Speed</td> <td>' + speed + ' </td>\n' 
			+ '<td>Distance to Target</td> <td>' + repr(round(distance_to_target, 1)) + ' m</td>\n' 
			+ '<td>Current Lat/Lon</td> <td>' + repr(round(current_lat, 6)) + ', ' + repr(round(current_long, 6)) + ' </td>\n' 
			+ '<td>Target Lat/Lon</td> <td>' + repr(round(target_lat, 6)) + ', ' + repr(round(target_long, 6)) + ' </td>\n' 
			+ '<td>Satellites in use </td> <td>' + sats_used 
			+ "&nbsp;&nbsp; (position error " + str(round(recentEpxy, 1))+ ' m)</td>\n')
		buoy_info.close()
	else:
		motorStop()
