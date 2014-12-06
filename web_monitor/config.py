import os,logging,copy

data_dir = os.path.join(os.curdir,'data')

logging_options = {
	"format" : '%(asctime)s :: %(levelname)s :: %(message)s',
	"backup_count" : 1,
	"mode" : "a", 		#append
	"max_size" : 1000000,	#1 MB
	"file_level" : logging.DEBUG, 
	"stdout_level" : logging.DEBUG,
	"extension" : ".log",
}

webmonitor_logging_options = copy.copy(logging_options)
webmonitor_logging_options["stdout_level"] = logging.INFO
webmonitor_logging_options["file_level"] = logging.DEBUG

scheduler_interval = 600
