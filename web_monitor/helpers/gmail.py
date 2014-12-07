#!/usr/bin/python

import config

import httplib2

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run

import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os

from apiclient import errors

def _authorize(opts = config.gmail_options):
	STORAGE = Storage(opts["storage"])

	# Start the OAuth flow to retrieve credentials
	flow = flow_from_clientsecrets(opts["secret_file"], scope=opts["oauth_scope"])
	http = httplib2.Http()

	# Try to retrieve credentials from storage or run the flow to generate them
	credentials = STORAGE.get()
	if credentials is None or credentials.invalid:
		credentials = run(flow, STORAGE, http=http)

	# Authorize the httplib2.Http object with our credentials
	http = credentials.authorize(http)

	# Build the Gmail service from discovery
	gmail_service = build('gmail', 'v1', http=http)

	return gmail_service

def send_mail(sender, to, subject, content, opts = config.gmail_options):
	gmail_service = _authorize(opts)
	message = _CreateMessage(sender,to,subject,content)

	_SendMessage(gmail_service,"me",message)

def _SendMessage(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print 'Message Id: %s' % message['id']
    return message
  except errors.HttpError, error:
    print 'An error occurred: %s' % error

def _CreateMessage(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_string())}
