#!/usr/bin/env bash

# Add Deadsnakes repo for Python 3 support
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt-get update

sudo apt-get install nginx -y
