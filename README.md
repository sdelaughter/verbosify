# verbosify
Run a bash script and send email and OS X notifications about its exit status

######1. Edit command.sh so that it contains the actual bash command(s) you want to run

######2. Edit settings.json
 - You should be able to configure all settings through this file, without having to modify the python script in any way.
 - Note that this must be a properly formatted JSON file, with no comments, no blank lines, etc. 
   - An overview of the JSON syntax can be found here: http://www.w3schools.com/json/json_syntax.asp
 - command_path and log_directory are both optional.  You should only enter values there if you need to override the default values, otherwise leave them as an empty set of quotes.  The defaults are determined at runtime, relative to the location of the python script, and a log directory will be created if it does not yet exist.  If you do want to override these defaults, you may include '~' to represent the user's home directory, and the python script will expand it to the full path.  That said, it's probably safer to just specify the full paths.
 - The comments section offers a place to add extra information to the body of the emails sent.  You may add any new key/value pairs you like to this section (you should be able to add lists and dictionaries too, but they're unlikely to be displayed nicely), remove any default entries you don't need, and even remove the comments section altogether if you want to.
 - Make sure the smtp_server, smtp_port, username, and password values in the email section are all properly set -- otherwise it will not be able to send emails.  The default values for smtp_port, username, and password are all blank since many smtp servers do not require authentication.
 - starttls is a boolean value, either 0 to turn it off or 1 to turn it on
 - Make sure to keep to_addr as a list in both the success and failure email sections, even if it only contains one value.
 - The notification section allows you to customize the OS X system notifications.
   - The 'enable' value toggles system notifications (0 to disable, 1 to enable)
     - Note that this should only be enabled on OS X with terminal-notifier installed, though it will fail gracefully otherwise
   - If the 'subtitle' value is left as an empty string, it will display the timestamp of when the command finished running
   
######3. Install terminal-notifier if you'd like to make use of OSX system notifications
    sudo gem install terminal-notifier

######4. Configure run.sh
  - Only necessary if you plan to run verbosify as a scheduled command (eg. with cron or launchd)
  - The included run.sh file assumes that it's in the same directory as verbosify.py and runs it with python (with no arguments)
  - Feel free to remove the directory detection if you'd prefere to specify an absolute path (if run.sh and verbosify.py are in different folders), and to add any command-line arguments you want.

######5. Copy the entire verbosify directory to wherever you'd like
  - I'd recommend ~/bin
 
###Supported command-line arguments
 - Accepts an optional '-c' or '--command' argument followed by the path of a command file to run
	  - If left out, it will use the value in settings.json'
	  - If the value in settings.json is an empty string, it will look for a command.sh file in the directory of this script
 - Accepts an optional '-l' or '--log' argument followed by the path of a log directory to use
   -	If left out, it will use the value in settings.json'
   -	If the value in settings.json is an empty string, it will look for a logs subdirectory in the directory of this script
	    - If that directory does not exist, it will be created
	  - Note that log file names are generated at runtime based on the starting timestamp
 - Accepts an optional '-L' or '--log_level' argument followed by the logging level to use
	  - If left out, it will use the value in settings.json'
	  - If the value in settings.json is an empty string, it will default to the INFO level
	  - If an invalid level is supplied by any means, it will default to the DEBUG level
	  - Lowercase or mixed-case arguments will be recognized and converted to the proper uppercase format
 - Accepts an optional '-q' or '--quiet' flag to only notify about failures, not successes
 - Accepts an optional '-s' or '--settings' argument followed by the path of a settings file to read
	  - If left out, it will look for a settings.json file in the directory of this script
 - Accepts an optional '-V' or '--version' flag to print the version number and exit
