#!/bin/bash

loc=`pwd`
SCRIPT_PATH="${loc}/run.sh"
function write_old_cron {
    lines=`crontab -l | grep -v "@daily . $SCRIPT_PATH" | grep -v "SHELL" | grep -v "PATH"`
    echo "$lines" >> tmp.cron
    crontab tmp.cron
    rm tmp.cron
}

# uninstall dependency
if [ -f /usr/local/bin/whereami ]; then 
    rm -f /usr/local/bin/whereami
    echo "Successfully uninstalled whereami program..."
else
    echo "whereami program has already been deleted"
fi 

# remove script
if [ -f "run.sh" ]; then 
    rm -f "run.sh"
    echo "Successfully uninstalled run.sh script..."
else 
    echo "run.sh has already been deleted"
fi


# remove cron file
if [ -f "weather.cron" ]; then
    rm -f "weather.cron"
    echo "Successfully uninstalled cron job..."
else 
    echo "weather.cron has already been deleted"
fi

# remove cron job
write_old_cron






