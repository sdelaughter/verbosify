#!/bin/bash

rsync -azvR $HOME/* $USER@fileserv.chem.umass.edu:rsync_backup/$HOSTNAME/
