#!/usr/bin/env bash

if ( sudo systemctl status compass | grep active ); then sudo systemctl stop compass; fi
