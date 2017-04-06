def setup():
    RPIO.setup(4, RPIO.IN) #pin 4 will be an I/O input pin - leak detection circuit

def checkForLeak()
	leak_input = RPIO.input(4)
	if leak_input == False:
		#shuts down the thrusters and sends leak alert to contol pad
		leak_alert = open('/home/pi/data_from_buoy/leak.txt', 'w')
		leak_alert.close()
		motorStop()
