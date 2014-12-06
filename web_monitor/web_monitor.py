# -- coding: utf-8 --
import alerts,config
from helpers.loggers import AddLogger
import os,importlib,logging

site_handlers = "site_handlers."

logger = logging.getLogger()
# on met le niveau du logger à DEBUG, comme ça il écrit tout
logger.setLevel(logging.DEBUG)

rootlogger = AddLogger("web_monitor","main").logger

def get_handler_obj(module_name,class_name,alert_name,url):
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

if __name__ == "__main__":
        #dfthdlr = LeBonCoinHandler(os.path.join(os.curdir,'data'),'testlbc','http://www.leboncoin.fr/voitures/offres/rhone_alpes/?f=a&th=1&ps=9&pe=15&rs=2008&fu=1')
	#dfthdlr.run()
	#print(dfthdlr.log_message())

	rootlogger.debug("read alerts")
	for name,item in alerts.items.iteritems():
		site_handler = item["site_handler"]
		(module_name,class_name) = site_handler.split(".")

		url = item["url"]

		handler_obj = get_handler_obj(module_name,class_name,name,url)

		rootlogger.debug("Alert name=%s,handler=%s,url=%s",name,module_name,url)	
		handler_obj.run()

		handler_obj.log()

