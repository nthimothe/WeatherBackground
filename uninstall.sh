#!/bin/bash

# uninstall dependency
if [ -f /usr/local/bin/whereami ]; then 
    rm -f /usr/local/bin/whereami
    echo "Successfully uninstalled whereami program"
fi 

# remove script
if [ -f "run.sh" ]; then 
    rm -f "run.sh"
    echo "Successfully uninstalled run.sh script"
fi


# remove cron job
if [ -f "weather.cron" ]; then
    rm -f "weather.cron"
    echo "Successfully uninstalled cron job"
fi






