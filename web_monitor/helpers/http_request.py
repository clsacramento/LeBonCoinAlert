# -- coding: utf-8 --
import pycurl
from StringIO import StringIO
from unidecode import unidecode

class HttpRequest:
	def __init__(self, url, args = "", fileName = None, method='get'):
		self.url = url
		self.args = args
		self.fileName = fileName
		self.method = method

		self._request()

		if fileName is not None:
			fp = open(fileName,'w')
			fp.write(self.output)
			fp.close()

	def _request(self):
		buffer = StringIO()
                c = pycurl.Curl()
		
		if(self.method.upper() == "GET"):
			url = self.url + self.args
		else:
			url = self.url
			c.setopt(c.POSTFIELDS, self.args)

                c.setopt(c.URL, url)
                c.setopt(c.WRITEDATA, buffer)
                c.perform()

		self.response_code = c.getinfo(c.RESPONSE_CODE)
		self.total_time = c.getinfo(c.TOTAL_TIME)

                c.close()

                self.output = unicode(buffer.getvalue(),errors="replace")

if __name__ == "__main__":
	#http = HttpRequest('https://www.google.fr/','search?q=test&oq=test&aqs=chrome..69i57j69i65l2j69i60j69i61l2.694j0j7&sourceid=chrome&es_sm=119&ie=UTF-8&qscrl=1',method='GET')
	http = HttpRequest("www.leboncoin.fr")
	print(http.output)
