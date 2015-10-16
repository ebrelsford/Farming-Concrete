#!/bin/bash
echo "Starting send_mail"
source $HOME/.bash_profile
workon fc
django-admin send_mail
echo "Finishing send_mail"
