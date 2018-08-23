#!/usr/bin/env bash

# Install libmysqlclient-dev which is used by mysqlclient pip package
sudo apt-get install libmysqlclient-dev -y

# Update deployment environment in uwsgi config file
sudo sed -i '/^deploy_env =/{h;s/=.*/= '"${DEPLOYMENT_GROUP_NAME,,}"'/};
${x;/^$/{s//deploy_env = '"${DEPLOYMENT_GROUP_NAME,,}"'/;H};x}' /opt/centive/launchpad/extras/uwsgi/launchpad.ini

# Install Python 3.6 and create virtual environment
sudo apt-get install python3.6 python3.6-venv -y
sudo apt-get install build-essential libssl-dev libffi-dev python3.6-dev -y
sudo -H pip3.6 install uwsgi
sudo -H pip3.6 install --upgrade pip
cd /home/ubuntu
mkdir pyvenvs
cd pyvenvs
sudo rm -rf launchpad
python3.6 -m venv launchpad

# Activate virtual environment
source /home/ubuntu/pyvenvs/launchpad/bin/activate
# Upgrade pip
pip install --upgrade pip
# Install setuptools & distribute
pip install -U setuptools
pip install -U distribute
# Resolve dependencies
pip install -r /opt/centive/launchpad/requirements.txt
# Export the config file path temporarily
export LAUNCHPAD_CONFIG_FILE=/opt/centive/launchpad-config/${DEPLOYMENT_GROUP_NAME,,}.env
# Collect static files
cd /opt/centive/launchpad
python3 project/manage.py collectstatic --clear --link --no-post-process --noinput
sudo chown -R ubuntu:www-data /opt/centive/launchpad/project/static
# Do migration
python3 project/manage.py makemigrations
python3 project/manage.py migrate
# Unset the config file path
unset LAUNCHPAD_CONFIG_FILE
# Deactivate virtual environment
deactivate

sudo ln -sf /etc/nginx/sites-available/launchpad /etc/nginx/sites-enabled
