import config
from helpers import gmail

import os,importlib

def gmail_notify(notification,subject,message):
	sender = notification["from"]
	to = notification["to"]
	content = notification["name"]+",\n"+message
 	print sender,to,subject,content
	gmail.send_mail(sender,to,subject,content)


notifiers = {
	"gmail_notify" : gmail_notify,
}

def send_notification(receiver,subject,message):
	notifier = receiver["type"]
	notifiers[notifier](receiver,subject,message)

