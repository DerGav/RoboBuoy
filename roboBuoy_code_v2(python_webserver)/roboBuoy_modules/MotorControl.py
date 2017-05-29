'''
Motor Control module

first run "setup()"
then run "thrust_strong()","thrust_soft()", "thrust_stop()" to control
forward thruster or "turn_right()", "turn_leftt()", "turn_stop()" to control
turn thruster
'''
from RPIO import PWM
import RPi.GPIO as GPIO
import time

# forward_thruster_pin = 17
# turn_thruster_pin = 18

forward_thruster_pin = 17
turn_thruster_pin = 27

LEFT_LED = 25
RIGHT_LED = 27
POWER_LED = 24


dma = 0
start = 10

# Thrust magnitude control
THRUST_OFF = 150
THRUST_SOFT = 160
THRUST_STRONG = 175
# Turn power
TURN_RIGHT = 145
TURN_LEFT = 155
TURN_OFF = 150


def thrust_strong():
	#speed = 'Going fast' + dist_text
	PWM.add_channel_pulse(dma, forward_thruster_pin, start, THRUST_STRONG)
	#GPIO.output(POWER_LED, GPIO.HIGH)

def thrust_soft():
	#speed = 'Approaching target' + dist_text
	PWM.add_channel_pulse(dma, forward_thruster_pin, start, THRUST_SOFT)
	#GPIO.output(POWER_LED, GPIO.HIGH)

def thrust_stop():
	#speed = 'Close to target' + dist_text
	# stop?
	PWM.add_channel_pulse(dma, forward_thruster_pin, start, THRUST_OFF)
	#GPIO.output(POWER_LED, GPIO.LOW)

def turn_stop():
	PWM.add_channel_pulse(dma, turn_thruster_pin, start, TURN_OFF)
	#GPIO.output(LEFT_LED, GPIO.LOW)
	#GPIO.output(RIGHT_LED, GPIO.LOW)

def turn_right():
	PWM.add_channel_pulse(dma, turn_thruster_pin, start, TURN_RIGHT)
	#GPIO.output(RIGHT_LED, GPIO.HIGH)
	#GPIO.output(LEFT_LED, GPIO.LOW)

def turn_left():
	PWM.add_channel_pulse(dma, turn_thruster_pin, start, TURN_LEFT)
	#GPIO.output(RIGHT_LED, GPIO.LOW)
	#GPIO.output(LEFT_LED, GPIO.HIGH)

def stop_turn_thrust():
	PWM.add_channel_pulse(dma, forward_thruster_pin, start, THRUST_OFF)
	time.sleep(1)
	PWM.add_channel_pulse(dma, turn_thruster_pin, start, TURN_OFF)
	time.sleep(1)

def setup():
   # GPIO.setmode(GPIO.BCM)
   # GPIO.setup(POWER_LED, GPIO.OUT)
   # GPIO.setup(RIGHT_LED, GPIO.OUT)
   # GPIO.setup(LEFT_LED, GPIO.OUT)

   PWM.setup()
   PWM.set_loglevel(PWM.LOG_LEVEL_ERRORS)
   PWM.init_channel(dma)
   PWM.add_channel_pulse(dma, forward_thruster_pin, start, THRUST_OFF)
   time.sleep(1)
   PWM.add_channel_pulse(dma, turn_thruster_pin, start, TURN_OFF)
   time.sleep(1)

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

def calculateTurnAngle():
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
