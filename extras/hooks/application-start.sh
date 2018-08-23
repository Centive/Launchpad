#!/usr/bin/env bash

sudo systemctl start compass | sudo systemctl restart compass
sudo systemctl start nginx | sudo systemctl restart nginx

sudo systemctl enable compass
sudo systemctl enable nginx