from RPIO import PWM
import RPi.GPIO as GPIO
import time

forward_thruster_pin = 17
turn_thruster_pin = 18
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
    GPIO.output(POWER_LED, GPIO.HIGH)

def thrust_soft():
    #speed = 'Approaching target' + dist_text
    PWM.add_channel_pulse(dma, forward_thruster_pin, start, THRUST_SOFT)
    GPIO.output(POWER_LED, GPIO.HIGH)

def thrust_stop():
    #speed = 'Close to target' + dist_text
    # stop?
    PWM.add_channel_pulse(dma, forward_thruster_pin, start, THRUST_OFF)
    GPIO.output(POWER_LED, GPIO.LOW)

def turn_stop():
    PWM.add_channel_pulse(dma, turn_thruster_pin, start, TURN_OFF)
    GPIO.output(LEFT_LED, GPIO.LOW)
    GPIO.output(RIGHT_LED, GPIO.LOW)

def turn_right():
    PWM.add_channel_pulse(dma, turn_thruster_pin, start, TURN_RIGHT)
    GPIO.output(RIGHT_LED, GPIO.HIGH)
    GPIO.output(LEFT_LED, GPIO.LOW)

def turn_left():
    PWM.add_channel_pulse(dma, turn_thruster_pin, start, TURN_LEFT)
    GPIO.output(RIGHT_LED, GPIO.LOW)
    GPIO.output(LEFT_LED, GPIO.HIGH)

def stop_turn_thrust():
    PWM.add_channel_pulse(dma, forward_thruster_pin, start, THRUST_OFF)
    time.sleep(1)
    PWM.add_channel_pulse(dma, turn_thruster_pin, start, TURN_OFF)
    time.sleep(1)

def setup():
   GPIO.setmode(GPIO.BCM)
   GPIO.setup(POWER_LED, GPIO.OUT)
   GPIO.setup(RIGHT_LED, GPIO.OUT)
   GPIO.setup(LEFT_LED, GPIO.OUT)	

   PWM.setup()
   PWM.set_loglevel(PWM.LOG_LEVEL_ERRORS)
   PWM.init_channel(dma)
   PWM.add_channel_pulse(dma, forward_thruster_pin, start, THRUST_OFF)
   time.sleep(1)
   PWM.add_channel_pulse(dma, turn_thruster_pin, start, TURN_OFF)
   time.sleep(1)
