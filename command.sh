#!/bin/sh

rsync -azvR $HOME/foo $USER@fileserv.chem.umass.edu:rsync_backup/
