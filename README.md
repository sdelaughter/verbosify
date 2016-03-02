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