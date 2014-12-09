# -- coding: utf-8 --
from default_handler import DefaultHandler
from helpers.http_request import HttpRequest
from unidecode import unidecode
import bs4 as BeautifulSoup
import os,re

class LeBonCoinHandler(DefaultHandler):
	handler_name = "lbc_handler"

	def __init__(self,path, name, url, args = "", method='get'):
		DefaultHandler.__init__(self,path,name,url,args,method)

	def run(self):
		tmpfile = os.path.join(self.path,"tmp")
		http = HttpRequest(self.url,self.args,method=self.method)
		
		self._parse_lbc(tmpfile)
		
		if os.path.isfile(self.last_filename):
                        os.rename(tmpfile,self.new_filename)
			self.diff()
                else:
			os.rename(tmpfile,self.last_filename)

	def _parse_lbc(self,output_file):
		http = HttpRequest(self.url,self.args,method=self.method)

                soup = BeautifulSoup.BeautifulSoup(http.output)
                lbcdiv = soup.find('div',attrs={'class':'list-lbc'})
                ads = lbcdiv.findAll("a")

                opf = open(output_file,"w")

                for ad in ads:
                        text = ad.text
                        retext = re.sub('\s+',' ',text)
                        line = unidecode(retext+ad['href']+"\n")
                        opf.write(line)

                opf.close()

	def new_ads(self):
		return len(self.added_lines)>0	

	def log(self):
		if self.new_ads():
			#TODO:
			#Fix: might advertise an old ad as new if a recent one is deleted.
                	print str(len(self.added_lines))+" new ad(s)."
		        self.logger.info(str(len(self.added_lines))+" new ad(s).")
			self.logger.info(str(self.added_lines))
                else:
			self.logger.debug("Nothing new.")

	def notification_items(self):
                return { "found_changes" : self.found_changes(),
                        "new_ads" : self.added_lines,
                        "deleted_ads" : self.deleted_lines,}
