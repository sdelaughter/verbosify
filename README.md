# verbosify
Run a bash script and send email and OS X notifications about its exit status

###Install and Configure

######1. Edit command.sh so that it contains the actual bash command(s) you want to run

######2. Edit settings.json
 - You should be able to configure all settings through this file, without having to modify the python script in any way.
 - Note that this must be a properly formatted JSON file, with no comments, no blank lines, etc.
   - An overview of the JSON syntax can be found here: http://www.w3schools.com/json/json_syntax.asp
 - command_path
   - This value is optional -- if left as a set of empty double quotes, it will default to a file named 'command.sh' in the same directory as the python script.
 - log_directory
   - This value is optional -- if left as a set of empty double quotes, it will default to a directory named 'logs' in the same directory as the python script.
   - If the 'logs' directory does not exist in this location, it will be created.
 - log_level
   - This value is optional -- if left as a set of empty double quotes, it will default to 'INFO'.
   - The full set of valid options are: 'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', and 'NOTSET'.
   - Lowercase and mixed-case values will be accepted and corrected to the proper all-caps formatting.
   - If an invalid value is supplied, it will default to 'DEBUG'.
 - comments
   - This section offers a place to add extra information to the body of the notification emails.
   - You may add any new key/value pairs you like to this section.  You should be able to add lists and dictionaries too, but they're unlikely to be displayed nicely.
   - You may also remove any default entries you don't need, and even remove the comments section altogether if you want to.  However, if you do leave the comments section in place you must also leave the 'success' and 'failure' dictionaries within it.
 - mail
   - Make sure the smtp_server, smtp_port, username, and password values in the email section are all properly set -- otherwise it will not be able to send emails.
   - The default values for smtp_port, username, and password are all blank by default since many smtp servers do not require authentication.
   - starttls is a boolean value, either 0 to turn it off or 1 to turn it on
   - Make sure to keep to_addr as a list in both the success and failure email sections, even if it only contains one value.
 - notification
   - This section allows you to customize the OS X system notifications.
     - The 'enable' values toggle system notifications (0 to disable, 1 to enable)
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
  
###Run
    cd /path/to/verbosify/
    python verbosify.py
 
###Command-Line Arguments
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
	  - If an invalid value is supplied, it will default to the DEBUG level
	  - Lowercase or mixed-case arguments will be recognized and converted to the proper uppercase format
 - Accepts an optional '-q' or '--quiet' flag to only notify about failures, not successes
 - Accepts an optional '-s' or '--settings' argument followed by the path of a settings file to read
	  - If left out, it will look for a settings.json file in the directory of this script
 - Accepts an optional '-V' or '--version' flag to print the version number and exit
