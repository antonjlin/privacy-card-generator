from installer import*

dependencies = 'datetime,termcolor,colorama'.split(',')
i  = Installer(dependencies=dependencies)
i.load()

from datetime import datetime
from termcolor import cprint, colored
import colorama


colorama.init()
'''
	Available text colors:
	red, green, yellow, blue, magenta, cyan, white.
        
'''
## normal logging function - time and text
def log(text):
	print("[{}] - {}".format(stamp(), text))

## colored logging function - time and text in color
def cLog(value, color):
	text = colored(value, color)
	print('[{}] - {}'.format(stamp(), text))

def taskLog(tasknum,text):
	print("[Task {}] - [{}] - {}".format(str(tasknum),stamp(), text))

## colored logging function - time and text in color
def taskCLog(tasknum,value, color):
	text = colored(value, color)
	print('[Task {}] - [{}] - {}'.format(str(tasknum),stamp(), text))
## colored printing function - text in color
def cPrint(value, color):
	text = colored(value, color)
	print(text)

## used to get the time wrapped in square brackets
def stamp():
    timestamp = str(datetime.now().strftime("%H:%M:%S.%f")[:-3])
    return timestamp

## just fetches the time (no square brackets)
def rawStamp():
	timestamp = datetime.now().strftime("%H:%M:%S")
	return timestamp








