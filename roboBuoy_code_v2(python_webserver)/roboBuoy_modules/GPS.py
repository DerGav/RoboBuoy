import threading

# import gps library somehow
# from gps import *

class GpsController(threading.Thread):
	def __init__(self):
		print("here")
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

def setupGPS():
    gpsc = GpsController()
    gpsc.start()
    logger.info("GPS controller started.")

def read():
	current_lat = gpsc.fix.latitude
	current_long = gpsc.fix.longitude
	sats_used = str(gpsc.satellitesUsed)

    # if logNow:
	# 	logger.debug("Long error (m): " + str(gpsc.fix.epx))
	# 	logger.debug("Lat  error (m): " + str(gpsc.fix.epy))
	# 	recentEpxy = math.sqrt(gpsc.fix.epx*gpsc.fix.epx + gpsc.fix.epy*gpsc.fix.epy)
	# 	logger.debug("Satellites used: " + sats_used + " position error " + str(round(recentEpxy, 1)))

def getDistanceToTarget():
	latMid = (current_lat + target_lat) / 2.0  # calc the midpoint of latitude
	m_per_deg_lat = 111132.954 - 559.822 * math.cos(2.0 * latMid) + 1.175 * math.cos(4.0 * latMid)
	m_per_deg_long = m_per_deg_lat * math.cos(latMid)
	deltaLatToTar = target_lat - current_lat # Gives +/- when appropriate to know where it's heading
	deltaLongToTar = target_long - current_long # Gives +/- when appropriate to know where it's heading
	distance_to_target = math.sqrt(math.pow(deltaLatToTar * m_per_deg_lat, 2) + math.pow(deltaLongToTar * m_per_deg_long, 2))

	if logNow:
		logger.info("Distance to target = " + str(distance_to_target))

def getDegreesBearingToTarget():
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
