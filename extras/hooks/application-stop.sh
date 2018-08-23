#!/usr/bin/env bash

if ( sudo systemctl status launchpad | grep active ); then sudo systemctl stop launchpad; fi
