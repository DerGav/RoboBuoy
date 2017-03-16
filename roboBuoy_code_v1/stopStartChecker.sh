#!/bin/bash
# Create a lock directory file to indicate whether this script is running.
if ! mkdir /tmp/robostarter.lock; then
	printf "Failed to acquire lock.\n" >&2
	exit 1
fi
trap 'rm -rf /tmp/robostarter.lock' EXIT # remove on exit.


echo "I will check for flag files"
while true
do
	if [ -f /home/pi/data_to_buoy/startScripts.txt ]
	then
		/home/pi/robo.sh start
		rm -rf /home/pi/data_to_buoy/startScripts.txt
	fi
	if [ -f /home/pi/data_to_buoy/restartScripts.txt ]
	then
		/home/pi/robo.sh restart
		rm -rf /home/pi/data_to_buoy/restartScripts.txt
	fi
	if [ -f /home/pi/data_to_buoy/stopScripts.txt ]
	then
		/home/pi/robo.sh stop
		rm -rf /home/pi/data_to_buoy/stopScripts.txt
	fi
	sleep 3
done
