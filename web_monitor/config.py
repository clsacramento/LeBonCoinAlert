import os,logging

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



