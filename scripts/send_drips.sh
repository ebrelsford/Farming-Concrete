#!/bin/bash
echo "Starting send_drips"
source $HOME/.bash_profile
workon fc
django-admin send_drips
echo "Finishing send_drips"