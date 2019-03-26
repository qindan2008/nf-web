#!/usr/bin/env bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit 1
fi

if [[ `uname -s` != "Linux" ]]
  then echo "This script is only for running on Linux"
  exit 1
fi

# This Linux-only script has only been tested on Ubuntu
# See https://docs.docker.com/compose/install/ for details on installing on Mac

curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
