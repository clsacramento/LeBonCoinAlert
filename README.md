LeBonCoinAlert
==============

Get notifications of new ads in leboncoin matching a specified criteria.

---------------

So, I was trying to by a car in France and I was using this leboncoin.fr site to look for car people are selling...
The thing is, I was finding it somewhat boring so I wrote a script to check if there were any new ads matching my criteria.
Well, I'm sharing the nasty script that I wrote, so if someone needs the samething it could be start. 
Then, if I get the time, I'll try to improve it to make it more modular, customizable and actually useful for other people...

How to use
----------
For now, to run it you may configure the desired url in the alerts.py file (you can have multiple alerts) then run python web_monitor.py
You need to put it in cron or something to make run from time to time...

Note: if it's not leboncoin site you can use default_handler but it won't pare the adds, just check the diffrences line by line...
