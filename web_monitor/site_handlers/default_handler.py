from helpers.http_request import HttpRequest
import os, difflib

class DefaultHandler:
	ADDED_SIGN = "+"
	DELETED_SIGN = "-"

	added_lines=[]
	deleted_lines=[]
	
	def __init__(self,path,name,url,args="",method='get'):
		self.path = path
		self.name = name
		self.url = url
		self.args = args
		self.method = method
		self.last_filename = os.path.join(path,name)
		self.new_filename = self.last_filename+"_"
	
	def run(self):
		if os.path.isfile(self.last_filename):
			http = HttpRequest(self.url,self.args,self.new_filename,self.method)
			self.diff()		
		else:
			http = HttpRequest(self.url,self.args,self.last_filename,self.method)

	def diff(self):
		lastfile = open(self.last_filename,"r")
		newfile = open(self.new_filename,"r")

		diff = difflib.Differ()
		self.diff_list = list(diff.compare(lastfile.readlines(),newfile.readlines()))

		
		self.deleted_lines = self.diff_lines(DefaultHandler.DELETED_SIGN)
		self.added_lines = self.diff_lines(DefaultHandler.ADDED_SIGN)

		os.rename(self.new_filename,self.last_filename)

	def found_changes(self):
		return (len(self.deleted_lines)+len(self.added_lines)>0)

	def diff_lines(self,diff_sign):
		lines = []
		for line in self.diff_list:
			if line[0] == diff_sign:
				lines.append(line.replace(diff_sign+" ",""))
		return lines

	def log_message(self):
		if self.found_changes():
			return "Changes found: "+str(len(self.added_lines))+" line(s) added and "+str(len(self.deleted_lines))+" lines(s) deleted."
		else:
			return "No changes found."

	def notification_items(self):
		return { "found_changes" : self.found_changes(),
			"added_lines" : self.added_lines,
			"deleted_lines" : self.deleted_lines,}
