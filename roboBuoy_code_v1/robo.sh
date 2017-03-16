#!/bin/sh
cmd=$1
case "$cmd" in
start)
	echo "Starting voltage monitor and motor control."
	sudo nohup python voltageInterrupt.py &
	sudo nohup python motor_control_3.py &
	;;
stop)
	echo "Killing ALL python processes!"
	sudo killall python
	;;
restart)
	echo "Killing ALL python processes!"
	sudo killall python
	echo "Starting voltage monitor and motor control."
	sudo nohup python voltageInterrupt.py &
	sudo nohup python motor_control_3.py &
	;;
*)	echo Invalid command "$cmd"
	exit 1
	;;
esac
