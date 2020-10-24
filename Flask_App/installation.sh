#!/bin/bash

sudo apt-get update
# mySQL module
apt-get install -y python-mysqldb
# Flask module
apt-get install python3-pip python3-dev nginx
sudo pip3 install virtualenv
pip install flask
# requests module
apt-get install -y python-requests