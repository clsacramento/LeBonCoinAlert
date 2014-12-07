# -- coding: utf-8 --
import alerts,notifications,notifier,config
from helpers.loggers import AddLogger
import os,importlib,logging
from apscheduler.schedulers.blocking import BlockingScheduler

site_handlers = "site_handlers."

logger = logging.getLogger()
# on met le niveau du logger à DEBUG, comme ça il écrit tout
logger.setLevel(logging.DEBUG)

rootlogger = AddLogger("web_monitor","main",config.webmonitor_logging_options).logger
apslogger = AddLogger("apscheduler","scheduler",config.webmonitor_logging_options).logger
exelogger = AddLogger("apscheduler","executors.default",config.webmonitor_logging_options).logger
apilogger = AddLogger("googleapiclient","discovery",config.webmonitor_logging_options).logger

class WebMonitor:
	def get_handler_obj(self,module_name,class_name,alert_name,url):
		class_ = None
		path = os.path.join(config.data_dir,module_name)
		try:
			os.stat(path)
		except:
			os.mkdir(path) 
		try:
			module_ = importlib.import_module(site_handlers+module_name)
			try:
				logger = AddLogger(module_name,alert_name).logger
				class_ = getattr(module_, class_name)(path,alert_name,url)
				class_.logger = logger
	        	except AttributeError:
				rootlogger.error('Class does not exist: '+class_name)
		except ImportError:
			rootlogger.error('Module does not exist: '+module_name)
		return class_ 

	def run(self):
		rootlogger.info(str(len(alerts.items))+" alerts configured.")
		self.check_alerts()

	def check_alerts(self):
	        for name,item in alerts.items.iteritems():
	                site_handler = item["site_handler"]
	                (module_name,class_name) = site_handler.split(".")
	
	                url = item["url"]
	
			handler_obj = self.get_handler_obj(module_name,class_name,name,url)
	
			rootlogger.debug("Alert %s,handler=%s,url=%s",name,module_name,url)        
	                handler_obj.run()

	                handler_obj.log()

			if(handler_obj.found_changes()):
				self.send_alert(item,handler_obj)

	def send_alert(self,item,handler_obj):

			alert_receivers = item["receivers"]

			notification_items = handler_obj.notification_items()

			alert_notification_item = item["notification_item"]

			notification_info = notification_items[alert_notification_item]
				
			rootlogger.info("Sending alert to receivers:"+str(notification_info))

			for alert_receiver in alert_receivers:
				receiver = notifications.receivers[alert_receiver]
				
				notifier.send_notification(receiver,item["description"],str(notification_info))

				rootlogger.debug("Alert sent to receiver: "+str(receiver))

def start_monitor():
	rootlogger.info("Starting web_monitor")
	web_mntr = WebMonitor()
	web_mntr.run()

def job():
	print "x"
	rootlogger.error("test")

if __name__ == "__main__":
        #dfthdlr = LeBonCoinHandler(os.path.join(os.curdir,'data'),'testlbc','http://www.leboncoin.fr/voitures/offres/rhone_alpes/?f=a&th=1&ps=9&pe=15&rs=2008&fu=1')
	#dfthdlr.run()
	#print(dfthdlr.log_message())

	
	scheduler = BlockingScheduler()
	scheduler.add_job(start_monitor, 'interval', seconds=config.scheduler_interval)

	try:
		scheduler.start()
	except (KeyboardInterrupt, SystemExit):
		rootlogger.warning("Stopping web_monitor")
 		pass
