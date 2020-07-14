#!/bin/bash


CRON_FILE="weather.cron"
loc=`pwd`

function preserve_cron {
   # take everything in cron that's not a path or a shell var and write it to tmp.cron
    old_cron=`crontab -l | grep -v "SHELL" | grep -v "PATH"`
    echo $old_cron >> $CRON_FILE
}

function add_shell {
    echo "SHELL=$SHELL" >> $CRON_FILE
}
function add_path {
    echo "PATH=$PATH" >> $CRON_FILE
}


# install whereami dependency
# if whereami has been moved, its been sent to the usr/local/bin
if [ -a "whereami-1.1.0.zip" ]; then
    unzip "whereami-1.1.0.zip"
    sleep 1
    mv whereami /usr/local/bin/whereami
    sleep 2
    echo "Successfully added whereami program..."
fi

# create the bash script to run if run.sh doesn't exist
if [ ! -f run.sh ]; then 
    # remember prev location in order to return to it 
    echo "curr=\`pwd\`" >> run.sh
    echo "placement=\"${loc}\"" >> run.sh
    echo "cd \$placement" >> run.sh
    echo "python3 weatherBackground.py" >> run.sh
    echo "cd \$curr" >> run.sh
    chmod 744 run.sh
    echo "Successfully wrote run.sh..."
else 
    echo "run.sh already exists..."
fi 


# add job to cron file if cron file doesn't yet exist
if [ ! -f $CRON_FILE ]; then
    # change background daily
    line="@daily . ${loc}/run.sh"
    preserve_cron
    add_shell
    add_path
    echo "$line" >> $CRON_FILE
    crontab $CRON_FILE
    echo "Successfully added cron job..."
else 
    echo "$CRON_FILE already exists..."
fi 