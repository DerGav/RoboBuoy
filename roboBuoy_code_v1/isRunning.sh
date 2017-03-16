#!/bin/bash

if pgrep motor_control > /dev/null
then
	echo "running"
else
	echo "stopped"
fi
