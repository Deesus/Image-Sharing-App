#!/bin/bash
apt-get -qqy update
apt-get -qqy install postgresql python-psycopg2
apt-get -qqy install python-flask python-sqlalchemy
apt-get -qqy install python-pip
pip install oauth2client
pip install requests
pip install flask-seasurf
su postgres -c 'createuser -dRS vagrant'
su vagrant -c 'createdb'
printf "\n\n\n"
echo "******  $(tput setaf 2)Setup complete$(tput setaf 7)  ******"
echo "Run $(tput setab 4)psql -f create_database.sql$(tput setab 0)"
echo "then $(tput setab 4)python start_server.py$(tput setab 0) to begin serving app"