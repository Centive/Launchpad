#!/usr/bin/env bash

# Install libmysqlclient-dev which is used by mysqlclient pip package
sudo apt-get install libmysqlclient-dev -y

# Update deployment environment in uwsgi config file
sudo sed -i '/^deploy_env =/{h;s/=.*/= '"${DEPLOYMENT_GROUP_NAME,,}"'/};
${x;/^$/{s//deploy_env = '"${DEPLOYMENT_GROUP_NAME,,}"'/;H};x}' /opt/piggymind/compass/extras/uwsgi/compass.ini

# Install Python 3.6 and create virtual environment
sudo apt-get install python3.6 python3.6-venv -y
sudo apt-get install build-essential libssl-dev libffi-dev python3.6-dev -y
sudo -H pip3.6 install uwsgi
sudo -H pip3.6 install --upgrade pip
cd /home/ubuntu
mkdir pyvenvs
cd pyvenvs
sudo rm -rf compass
python3.6 -m venv compass

# Activate virtual environment
source /home/ubuntu/pyvenvs/compass/bin/activate
# Upgrade pip
pip install --upgrade pip
# Install setuptools & distribute
pip install -U setuptools
pip install -U distribute
# Resolve dependencies
pip install -r /opt/piggymind/compass/requirements.txt
# Export the config file path temporarily
export COMPASS_CONFIG_FILE=/opt/piggymind/compass-config/${DEPLOYMENT_GROUP_NAME,,}.env
# Collect static files
cd /opt/piggymind/compass
python3 project/manage.py collectstatic --clear --link --no-post-process --noinput
sudo chown -R ubuntu:www-data /opt/piggymind/compass/project/static
# Do migration
python3 project/manage.py makemigrations
python3 project/manage.py migrate
# Unset the config file path
unset COMPASS_CONFIG_FILE
# Deactivate virtual environment
deactivate

sudo ln -sf /etc/nginx/sites-available/compass /etc/nginx/sites-enabled
