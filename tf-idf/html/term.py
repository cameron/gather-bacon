#! /home/shanxi/opt/bin/python
print "Content-type: text/html\r\n\r\n"

import header; db = header.db; form = header.form


if form.has_key('term'):
	
else:
	print "Need a term in the url (like <a href='?term=canon'>this</a>)."