# -- coding: utf-8 --
import config

import os,logging
from logging.handlers import RotatingFileHandler

class AddLogger:
	def __init__(self,handler_name,alert_name,opts = config.logging_options):
		# création de l'objet logger qui va nous servir à écrire dans les logs
	        self.logger = logging.getLogger(handler_name+"."+alert_name)
	
		# création d'un formateur qui va ajouter le temps, le niveau
		# de chaque message quand on écrira un message dans le log
	        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')

		log_dir = os.path.join(config.data_dir,handler_name)
		try:
			os.stat(log_dir)
		except:
			os.mkdir(log_dir)
		self.log_file = os.path.join(log_dir,alert_name+opts["extension"])

		# création d'un handler qui va rediriger une écriture du log vers
		# un fichier en mode 'append', avec 1 backup et une taille max de 1Mo
		self.file_handler = RotatingFileHandler(
			self.log_file, 
			opts["mode"],
			opts["max_size"],
			opts["backup_count"]
		)
		# on lui met le niveau sur DEBUG, on lui dit qu'il doit utiliser le formateur
		# créé précédement et on ajoute ce handler au logger
		self.file_handler.setLevel(opts["file_level"])
		self.file_handler.setFormatter(formatter)
		self.logger.addHandler(self.file_handler)
	 
		# création d'un second handler qui va rediriger chaque écriture de log
		# sur la console
		self.stream_handler = logging.StreamHandler()
		self.stream_handler.setLevel(opts["stdout_level"])
		self.stream_handler.setFormatter(formatter)
		self.logger.addHandler(self.stream_handler)

		self.logger.debug("start logging")	
