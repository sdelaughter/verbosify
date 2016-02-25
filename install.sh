#!/bin/sh

#Install terminal-notifier if not already installed
if ! gem list terminal-notifier -i
  sudo gem install terminal-notifier
fi

#Get the path for this installer's parent directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

#Create ~/bin/ if it doesn't already exist
mkdir -p $HOME/bin

#Copy files into place
cp -av "$DIR/verbosify" "$HOME/bin/"
