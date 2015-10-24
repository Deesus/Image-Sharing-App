#!/bin/bash
apt-get -qq -y update
apt-get -qq -y install postgresql python-psycopg2
apt-get -qq -y install python-flask python-sqlalchemy
apt-get -qq -y install python-pip

pip install oauth2client
pip install requests
pip install flask-seasurf

psql -f create_database.sql

find /image_sharing/uploaded -mtime -5  -ok  rm -f {} \;

printf "\n\n\n"
echo "******  $(tput setaf 2)Setup complete$(tput setaf 7)  ******"
echo "Run $(tput setab 4)python start_server.py$(tput setab 0) to begin serving app"
