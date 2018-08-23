#!/usr/bin/env bash

sudo systemctl start launchpad | sudo systemctl restart launchpad
sudo systemctl start nginx | sudo systemctl restart nginx

sudo systemctl enable launchpad
sudo systemctl enable nginx