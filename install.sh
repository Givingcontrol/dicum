#!/bin/sh

currentUser=$(whoami)

dicumFilePath="/var/dicum"
dicumFileName="dicum"

sudo mkdir $dicumFilePath &&
  cd $dicumFilePath &&
  sudo touch $dicumFileName &&
  sudo chown "$currentUser":"$currentUser" $dicumFileName &&
  echo "01/01/01 01:01:01" >$dicumFileName ||
  (
    echo "Installation Failed, could not create necessary files in $dicumFilePath, you'll have to clean that up yourself"
    exit
  )

mkdir -p /tmp/.dicum/html/
mkdir -p /tmp/.dicum/images/
