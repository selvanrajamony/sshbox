#!/bin/bash

LIST=`docker images | grep sshbox | awk {'print $2'}`
#echo $LIST

read -p "enter account name in the format \"aws-<account_name>\" :" accountname
echo "$accountname"

if echo $LIST | grep -w $accountname > /dev/null; then
    	echo "Images already exist"
else
    	echo "Creating image $accountname"
	docker build -t sshbox:$accountname .
	if [ $? -eq 0 ]; then
       		echo "sucessfully created image $accountname in sshbox repository"
	else
        	echo "failure in creating image $accountname in sshbox repository"
	fi
fi
exit 

