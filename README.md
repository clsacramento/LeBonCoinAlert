LeBonCoinAlert
==============

Get notifications of new ads in leboncoin matching a specified criteria.

---------------

So, I was trying to by a car in France and I was using this leboncoin.fr site to look for cars that people were selling...
The thing is, I was finding it somewhat boring so I wrote a script to check if there were any new ads matching my criteria.
Well, I'm sharing the nasty script that I wrote, so if someone needs the samething it could be a start point. 
Then, if I get the time, I'll try to improve it to make it more modular, customizable and actually useful for other people...

How to use
----------
For now, to run it you may configure the desired url in the alerts.py file (you can have multiple alerts) then run python web_monitor.py
```
  python web_monitor.py
```

Notes: 
  * if it's not leboncoin site you can use default_handler but it won't parse the adds, just check the diffrences, line by line...
  * before running check config.py see what you can change to make it work better for you.

### Notifications
For now, only email notifications via Gmail Google API is available. To use it, you need to configure a project on you Google Console: https://console.developers.google.com/project . Then enable Gmail API and configure an identification client for native applications, check the googleapi docs for help with this here: https://developers.google.com/gmail/api/quickstart/quickstart-python. When this is all set, download the client\_secret.json for this client. In config.py set the googleapi\_dir with directory where the file was saved.

To be able to receive email from alerts, you need to set at least one notifications.receiver (see notifications.py.example) to write you own customized notifications.py
```python
receivers = {
	"me" : {
		"name"	: "me",
		"type"	: "gmail_notify",
		"from"	: "me@gmail.com",
		"to"	: "me@gmail.com",
	}, 
}
```

On alerts.py, set the receivers for the alert item with a receiver that you configured, for example:
```python
items = {
	"lbc-tout" : { 
		"url" : "http://www.leboncoin.fr/voitures/offres/rhone_alpes/?f=a&th=1&ps=9&pe=15&rs=2008&fu=1", 
		"site_handler" : "lbc_handler.LeBonCoinHandler",
		"description" : "Tout voiture Rhone Alpes",
		"receivers" : ["me",],
		"notification_item" : "new_ads",
	},
}
```
