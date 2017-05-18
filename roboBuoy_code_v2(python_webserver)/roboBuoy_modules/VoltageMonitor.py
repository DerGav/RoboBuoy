# First two lines may already exist if this is merged into the main controller:
#import RPi.GPIO as GPIO
import time


class VoltageMonitor:
	def __init__(self, pin):
		self.batteryPin = pin
		self.slope = -11.399
		self.intercept = 21.52
		self.batLow = 14.2
		self.batDanger = 14.0
	def read_voltage():
		return voltageCheck(self.batteryPin,self.slope,self.intercept)

checkPi = False
debug = True

# At the top where other I/O pins are defined:
# Motor uses 18 and 17.
# PiBatteryPin = 22
# MotorBatteryPin = 23

batteryPin = 22

# Calibration
piSlope = -11.399
piIntercept = 21.52
motorSlope = -11.399
motorIntercept = 21.52

slope = -11.399
intercept = 21.52

# Limit levels
batLow = 14.2
batDanger = 14.0


# Maximum time to wait for a dead or disconnected battery
maxWait = 1000

# Be sure this does not interfere with other GPIO usage.  Set and reset??
GPIO.setmode(GPIO.BCM)


# Define function to measure charge time
# The key parts which wait for the interupt are based on code
# by Alex Eames, found at
# http://raspi.tv/2013/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio
# I (JSR) have added the timing calculations to make this useful
# for estimating battery voltage.
def CapacitorChargeTime (Pin):
  counter = 0
  # Discharge capacitor
  GPIO.setup(Pin, GPIO.OUT)
  GPIO.output(Pin, GPIO.LOW)
  # Tests with a sleep of only 0.001 were good, but with no delay
  # at all results are poor.
  time.sleep(0.01)
  GPIO.setup(Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  # Count loops until voltage across capacitor reads high on GPIO
  startT = time.time()
  try:
	channel = GPIO.wait_for_edge(Pin, GPIO.RISING, timeout=maxWait)
	if channel is None:
	  print('Timeout - dead battery or bad connection.')
	  return 1000.0
  except KeyboardInterrupt:
	GPIO.cleanup()
	return 0.0
  endT = time.time()
  # Return elapsed time in milliseconds, as a float.
  delta = (endT-startT)*1000
  return delta

def ToBrowser (msg1, msg2):
  buoy_info = open('/home/pi/data_from_buoy/battery.txt', 'w')
  if checkPi:
	buoy_info.write('<td>Pi Battery</td> <td>' + repr(msg1) + ' </td> \n')
  else:
	buoy_info.write('<td>Pi Battery</td> <td>Not monitored</td> \n')
  buoy_info.write('<td>Motor Battery</td> <td>' + repr(msg2) + ' </td> \n')
  buoy_info.close()

def ToRoboBuoy (msg1, msg2):
  buoy_info = open('/home/pi/data_to_buoy/battery.txt', 'w')
  if checkPi:
	buoy_info.write(msg1 + '\n')
  else:
	buoy_info.write("Pi not monitored\n");
  buoy_info.write(msg2 + '\n')
  buoy_info.close()

def median(list):
	list = sorted(list)
	if len(list) % 2 == 0:
		return (list[(len(list)/2)-1] + list[len(list)/2])/2.0
	elif len(list) % 2 != 0:
		return list[int((len(list)/2))]


def voltageCheck(pin, slope, intercept):
	# Taking the median of 5 calls to CCT gives much more stable results.
	chargeCount = median([CapacitorChargeTime(pin),
						  CapacitorChargeTime(pin),
						  CapacitorChargeTime(pin),
						  CapacitorChargeTime(pin),
						  CapacitorChargeTime(pin)])
	voltage = slope * chargeCount + intercept
	#if debug: print(repr(chargeCount) + "ms gives V = " + repr(voltage))
	print(repr(chargeCount) + "ms gives V = " + repr(voltage))
	return voltage

def check_roboBuoy_voltage():
	return voltageCheck(22, slope, intercept)
# if __name__ == '__main__':
#     print(CapacitorChargeTime(PiBatteryPin))

#
# #
# #  Check Raspberry Pi battery voltage
# #
# # Note that motorBatProblem serves a dual uses.  When false it means that no
# # problem has been detected yet.  Once a motor battery tests below the danger
# # level, the message will be stored here and it won't get updated until restart.
# # The variable will test logical True, so we can use it to skip voltage
# # checks.
# motorBatProblem = False
# pVoltage = 0.0
# mVoltage = 0.0
# msg1 = ""
# msg2 = ""
# while 1:
#     # Get voltages
#     if checkPi:
#       pVoltage = voltageCheck(PiBatteryPin, piSlope, piIntercept)
#     # If the motor battery is already marked dead don't check again.
#     if not motorBatProblem:
#       mVoltage = voltageCheck(MotorBatteryPin, motorSlope, motorIntercept)
#     if debug:
#       print("  Pi Voltage:    " + repr(pVoltage))
#       print("  Motor Voltage: " + repr(mVoltage))
#
#     # Check for actions.  Handle emergency conditions first, as
#     # we may not even need the rest of the code in those cases.
#     # Then do the rest so the browser gets an update and values
#     # are available to any other code which wants to look.
#     if checkPi:
#       if pVoltage < piBatDanger:
#         # Double check before drastic action
#         # If voltage is actually okay, we'll carry on with the new value.
#         # This assumes that a fraction of a second for checking won't be a disaster.
#         pVoltage = voltageCheck(PiBatteryPin, piSlope, piIntercept)
#         print("Pi retry voltage: " + repr(pVoltage) + "\n")
#         if pVoltage < piBatDanger:
#           ToRoboBuoy("EMERGENCY RoboBuoy STOP.  Pi voltage is " + repr(pVoltage),
#   		   repr(mVoltage))
#           ToBrowser("EMERGENCY RoboBuoy STOP. " + repr(pVoltage),
#                      repr(mVoltage))
#           # We'll be shutting down the Pi.  Might as well quit.
#           if debug: print(" send low Pi battery emergency stop")
#           quit()
#
#     # Similar code for the motor battery, but we'll shut down just the
#     # motors and not the Raspberry Pi.
#     if not motorBatProblem and (mVoltage < motorBatDanger):
#       # Double check before drastic action
#       # If voltage is actually okay, we'll carry on with the new value.
#       # This assumes that our low battery voltage isn't so finely set
#       # that a fraction of a second for checking will be a disaster.
#       mVoltage = voltageCheck(MotorBatteryPin, motorSlope, motorIntercept)
#       if mVoltage < motorBatDanger:
#         motorBatProblem = "EMERGENCY MOTOR STOP.  Motor voltage is " + repr(mVoltage)
#         ToRoboBuoy(repr(pVoltage), motorBatProblem)
#         ToBrowser(repr(pVoltage), motorBatProblem)
#         if debug: print(" send low Motor battery emergency stop")
#
#     # In non-emergency conditions we just set msg1 for the Pi and msg2
#     # for the motor battery and send them off to the web server.  The
#     # controller code just gets the numerical values.
#     # control code.
#     if checkPi:
#       if  pVoltage < piBatLow:
#         if debug: print(" send low Pi battery warning")
#         msg1 = "Low: " + repr(pVoltage)
#       else:
#         if debug: print(" Sending updated Pi voltage to browser")
#         msg1 = repr(pVoltage)
#
#     # Similar for motor battery, but no new voltage if it's dead.
#     if motorBatProblem:
#       msg2 = motorBatProblem
#     elif mVoltage < motorBatLow:
#       if debug: print(" send low motor battery warning")
#       msg2 = "Low: " + repr(mVoltage)
#     else:
#       if debug: print(" Sending updated motor voltage to browser")
#       msg2 = repr(mVoltage)
#
#     # Update what the browser displays and what the controller gets.
#     ToBrowser(msg1, msg2)
#     if motorBatProblem:
#       ToRoboBuoy(repr(pVoltage), motorBatProblem)
#     else:
#       ToRoboBuoy(repr(pVoltage), repr(mVoltage))
#     time.sleep(2)
