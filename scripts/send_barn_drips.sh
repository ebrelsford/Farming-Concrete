#!/bin/bash
echo "Starting send_barn_drips"
source $HOME/.bash_profile
workon fc
django-admin send_barn_drips
echo "Finishing send_barn_drips"
