#! /usr/bin/env python
print "Content-type: text/html\r\n\r\n"

import header; db = header.db; form = header.form



if form.has_key('id'):
	
	doc_id = form['id'].value.replace("\"","")
	
	db.execute("SELECT title,body FROM documents WHERE id=\"" + doc_id + "\";")
	title,body = db.fetchone()
	print "<div id='document'>"
	print "<h2>" + title + "</h2>"
	print "<p>" + body.replace("\n","<br>") + "</p>"
	print "</div>"
	
	

	# related document list
	num_docs = 10
	print "<div class='sidebar'>"
	sql = "SELECT scores2.doc2,scores2.score,documents.title FROM scores2,documents WHERE scores2.doc1=" + doc_id + " AND documents.id=scores2.doc2 ORDER BY score DESC LIMIT " + str(num_docs)
	db.execute(sql)
	if db.rowcount > 0:
		print "<h2>Top " + str(num_docs) + " related documents</h2><ul>"
		for doc2_id,score,doc2_title in db.fetchall():
			print "<li><a href='document.py?id=" + str(doc2_id) + "'>" + doc2_title + "</a></li>" 
	else:	
		print "No scores computed for this document."
	print "</div>"
	
	# top words
	num_docs = 10
	print "<div class='sidebar'>"
	sql = "SELECT term FROM document_tfs WHERE doc_id=\"" + str(doc_id) + "\" ORDER BY tfidf DESC LIMIT " + str(num_docs)
	db.execute(sql)
	if db.rowcount > 0:
		print "<h2>Top " + str(num_docs) + " Indicators</h2><ul>"
		for term in db.fetchall():
			print "<li><a href='index.py?query_string=" +  term[0] + "'>" +  term[0] + "</a></li>" 
	else:	
		print "There was an error with the sql query..."
	print "</div>"
	
else:
	print "Need a document id in the url (document.py?id=XXX -- with 1-4 x's) to display an article."	

print header.footer
