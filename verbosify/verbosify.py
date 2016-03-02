"""Last Updated 2/25/16
Written by Samuel DeLaughter
Departments of Chemistry and BMB
University of Massachusetts at Amherst

Runs a bash script and sends notifications about the result
Ideal for rsync backups or other scheduled tasks whose output would otherwise be unknown

Configure via settings.json, which should be in the same directory as this file (unless an alternate settings file is specified via the -s argument)

Accepts an optional '-c' or '--command' argument followed by the path of a command file to run
	If left out, it will use the value in settings.json'
	If the value in settings.json is an empty string, it will look for a command.sh file in the directory of this script
Accepts an optional '-l' or '--log' argument followed by the path of a log directory to use
	If left out, it will use the value in settings.json'
	If the value in settings.json is an empty string, it will look for a logs subdirectory in the directory of this script
	If that directory does not exist, it will be created
	Note that log file names are generated at runtime based on the starting timestamp
Accepts an optional '-L' or '--log_level' argument followed by the logging level to use
	If left out, it will use the value in settings.json'
	If the value in settings.json is an empty string, it will default to the INFO level
	If an invalid level is supplied by any means, it will default to the DEBUG level
	Lowercase or mixed-case arguments will be recognized and converted to the proper uppercase format
Accepts an optional '-q' or '--quiet' flag to only notify about failures, not successes
Accepts an optional '-s' or '--settings' argument followed by the path of a settings file to read
	If left out, it will look for a settings.json file in the directory of this script
Accepts an optional '-V' or '--version' flag to print the version number and exit

"""

__version__ = "0.1"

import argparse
from email.mime.text import MIMEText
import json
import logging
import logging.handlers
import os
import smtplib
import subprocess
import sys
import time


def get_log_level():
	if args.log_level:
		log_level = str(args.log_level)
	else:
		if SETTINGS['log_level'] == '':
			log_level = 'INFO'
		else:
			log_level = SETTINGS['log_level']
	log_level = log_level.upper()
	if log_level not in ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET']:
		log_level = 'DEBUG'
	print('Log level set to: ' + str(log_level))
	return log_level


def get_log_path(timestamp):
	if args.log:
		log_directory = args.log.name
	else:
		if SETTINGS['log_directory'] == '':
			log_directory = str(os.path.dirname(os.path.realpath(__file__))) + '/logs/'
		else:
			log_directory = SETTINGS['log_directory']
			
	if log_directory.startswith('~'):
		prefix = os.path.expanduser('~')
		log_directory = str(prefix) + log_directory.split('~')[1]
		
	if not os.path.exists(log_directory):
		os.makedirs(log_directory)
		
	log_filename = str(timestamp['filename']) + '.log'
	log_path = str(log_directory) + str(log_filename)
	print('Log path set to: ' + str(log_path))
	return log_path
	
def get_command_path():
	if args.command:
		command_path = args.command.name
		if '/' not in command_path:
		#If calling a command file in the current working directory, make sure it is preceeded by './'
			command_path = './' + str(command_path)
	else:
		if SETTINGS['command_path'] == '':
			command_path = str(os.path.dirname(os.path.realpath(__file__))) + '/test.sh'
		else:
			command_path = SETTINGS['command_path']
	if command_path.startswith('~'):
		prefix = os.path.expanduser('~')
		command_path = str(prefix) + command_path.split('~')[1]
	print('Command path set to: ' + str(command_path))
	return command_path


def notify(title, subtitle, message):
	"""Send an OS X System Notification

	Parameters
	----------
	title : string
		The notification's title
	subtitle : string
		The notification's subtitle
	message : string
		The notification's message
		
	Returns
	-------
	None
	
	"""
	t = '-title {!r}'.format(title)
	s = '-subtitle {!r}'.format(subtitle)
	m = '-message {!r}'.format(message)
	os.system('terminal-notifier {}'.format(' '.join([m, t, s])))
    

def send_email(status, output, error, startTime, endTime):
	"""Send Email

	Parameters
	----------
	status : string
		'success' if the task completed with no errors
		'failure' otherwise
	output : string
		The task's standard output
	error : string
		The task's error output
	startTime : dict
		The start time for the task, formatted by format_timestamp()
                
	Returns
	-------
	None

	"""
    
	print('Composing ' + str(status) + ' email')
	logging.debug('Composing ' + str(status) + ' email')
	
	endTime = format_timestamp(time.localtime())['display']
	
	body = SETTINGS['email'][status]['message']
	if 'comments' in SETTINGS:
		body += '\n'
		for k in SETTINGS['comments']:
			body += ('\n' + str(k) + ': ' + str(SETTINGS['comments'][k]))
	body += "\n\nStart Time: " + str(startTime['display'])
	body += "\n  End Time: " + str(endTime)
	body += "\n\nError Message:\n" + str(error)
	body += "\n\nFull Output:\n" + str(output)
	
	to_addr = SETTINGS['email'][status]['to_addr']
	from_addr = SETTINGS['email'][status]['from_addr']
	
	msg = MIMEText(body)
	msg['Subject'] = SETTINGS['email'][status]['subject']
	msg['To'] = ", ".join(to_addr)
	msg['From'] = from_addr
	
	if SETTINGS['email']['smtp_port'] != '':
		s = smtplib.SMTP(SETTINGS['email']['smtp_server'], SETTINGS['email']['smtp_port'])
	else:
		s = smtplib.SMTP(SETTINGS['email']['smtp_server'])
	if SETTINGS['email']['starttls']:
		s.starttls()
	if((SETTINGS['email']['username'] != '') and (SETTINGS['email']['password'] != '')):
		s.login(SETTINGS['email']['username'], SETTINGS['email']['password'])
	try:
		print('Sending Email')
		logging.info('Sending Email')
		s.sendmail(from_addr, to_addr, msg.as_string())
		print('Sent Email to ' + str(to_addr))
		loggin.info('Sent Email to ' + str(to_addr))
	except:
		logging.critical('FAILED TO SEND EMAIL TO: ' + str(to_addr))	
	s.quit()
	

def generate_notification(status, endTime):
	"""Generate an OS X System Notification

	Parameters
	----------
	status : string
		'success' if the task completed with no errors
		'failure' otherwise

	Returns
	-------
	None
	
	"""
	
	if status not in ['success', 'failure']:
		status = 'failure'
	print('Generating System Notification')
	logging.debug('Generating System Notification')
	title = SETTINGS['notification'][status]['title']
	subtitle = SETTINGS['notification'][status]['subtitle']
	if subtitle == '':
		subtitle = 'at ' + str(endTime['display'])
	message = SETTINGS['notification'][status]['message']
	try:
		notify(title, subtitle, message)
	except:
		logging.warning('Failed to generate system notification')


def format_timestamp(t):
	"""Send welcome emails to all new users

	Parameters
	----------
	t : time.struct_time
		A timestamp generated by time.localtime()

	Returns
	-------
	timestamp : dict
		A dictionary of differently formatted versions of the given timestamp

	"""

	timestamp={}
	
	timestamp['original'] = t
	
	t = [t[0], t[1], t[2], t[3], t[4], t[5]]
	timestamp['list'] = t
	
	for i in range(len(t)):
		if(len(str(t[i])) == 1):
			t[i] = ('0' + str(t[i]))
	timestamp['list-padded'] = t
	
	timestamp['filename'] = (str(t[0]) + '_' + str(t[1]) + '_' + str(t[2]) + '_' + str(t[3]) + '-' + str(t[4]) + '-' + str(t[5]))
	timestamp['display'] = (str(t[1]) + '/' + str(t[2]) + '/' + str(t[0]) + ' ' + str(t[3]) + ':' + str(t[4]) + ':' + str(t[5]))
	
	return timestamp


def main():
	"""Do Everything

	Parameters
	----------
	None
                
	Returns
	-------
	None

	"""

	#Parse arguments
	parser = argparse.ArgumentParser(description = 'Roster Import Script')
	parser.add_argument('-c', '--command', action='store', nargs='?', default=False, dest='command', type=file, help='command file')
	parser.add_argument('-l', '--log', action='store', nargs='?', default=False, dest='log', type=argparse.FileType('r'), help='log directory')
	parser.add_argument('-L', '--log_level', action='store', nargs='?', default=False, dest='log_level', help='specify logging level')
	parser.add_argument('-q', '--quiet', action='store_true', default=False, dest='quiet', help='Only email for successes, not failures')
	parser.add_argument('-s', '--settings', action='store', nargs='?', default=False, dest='settings', type=argparse.FileType('r'), help='settings file')
	parser.add_argument('-V', '--version', action='version', version=__version__)

	global args
	args = parser.parse_args()

	#Load settings
	if args.settings:
		SETTINGS_FILE = args.settings
	else:
		SETTINGS_FILE = str(os.path.dirname(os.path.realpath(__file__))) + '/settings.json'
	global SETTINGS	
	SETTINGS = json.load(open(SETTINGS_FILE))

	#Record and format a starting timestamp
	t = time.localtime()
	startTime=format_timestamp(t)
	
	#Set up logging
	print('Setting up log file')
	log_path = get_log_path(startTime)
	logging.basicConfig(filename=log_path,level=get_log_level(),format='%(levelname)s: %(message)s')
	#print(logging.getLogger().getEffectiveLevel())
	
	#Run the scheduled task and obtain both the standard output and error output
	print('Running the backup command...')
	logging.info('Running the backup command...')
	command_path = get_command_path()
	proc = subprocess.Popen(command_path.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout_value, stderr_value = proc.communicate()
	print 'Output:\n', stdout_value

	if stderr_value == '':
		print 'Command exited with no errors'
		logging.info('Command exited with no errors')
		status = 'success'
	else:
		print 'Command exited with error(s)'
		logging.warning('Command exited with error(s)')
		print 'Error:\n', stderr_value
		logging.warning('Error: ' + str(stderr_value))
		status = 'failure'
	
	endTime = format_timestamp(time.localtime())
	
	if((status == 'success') and (args.quiet)):
	#If the task completed with no errors and the --quiet flag is set, skip notifications
		pass
	else:
		send_email(status, stdout_value, stderr_value, startTime, endTime)
		if SETTINGS['notification']['enable']:
			generate_notification(status, endTime)
		
		
if __name__ == "__main__":
	main()