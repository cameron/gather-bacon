#! /home/shanxi/opt/bin/python

import xml.sax
import re
import MySQLdb

class PageHandler(xml.sax.handler.ContentHandler):
	def __init__(self,table,limit=-1):
		self.current_page = None
		self.inTitle = False
		self.inText = False
		self.buffer = ""
		
		self.counter = 0
		self.limit = limit
		
		self.table = table
		
		self.conn = MySQLdb.connect(	host = "dcm.exsupera.com",
										user = "shanxi",
										passwd = "tknpitoz",
										db = "exs_dcm")
		self.cursor = self.conn.cursor()
		self.cursor.execute( "TRUNCATE TABLE " + str(self.table))
		
	def startElement(self,name,attributes):

		if name == "title":
			self.inTitle = True
		elif name == "text":
			self.inText = True
	

2	def characters(self,data):
		if self.inTitle:
			self.current_page = data
		elif self.inText:
			self.buffer += data
	
	def endElement(self,name):
		if name == "title":
			self.inTitle = False
		elif name == "text":
			self.inText = False

			# clean the article text by striping, in this order, the following:
			# hyperlinks 
			# html tags
			# everything that is not [-A-Za-z0-9\n]
			self.buffer = re.sub("[^-\w\n]"," ",re.sub("<.*?>"," ",re.sub("http://.*?\s", "", self.buffer)))

			# make sure we're not including simple page redirects
			if self.buffer.strip().lower().find("redirect") != 0:
				sql = "INSERT INTO %s (title,body) VALUES (\"%s\",\"%s\")" % (self.table,self.current_page.encode('latin-1','replace').replace("\"",""),self.buffer.encode('latin-1','replace').replace("\"",""))
				self.cursor.execute(sql)

				
			self.buffer = ""
			self.counter += 1
			if self.limit != -1 and self.counter > self.limit:
				raise xml.sax.SAXException("Page limit reached while parsing.")


if __name__ == "__main__":

	parser = xml.sax.make_parser()
	handler = PageHandler(table="documents")
	parser.setContentHandler(handler)	
	
	try:
		parser.parse("wiki_top_articles.xml")
	except xml.sax.SAXException, e:
		print e
	
	print handler.counter
	
