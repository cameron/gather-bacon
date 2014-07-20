#! /usr/bin/env python
print "Content-type: text/html\r\n\r\n"

	
import header; db = header.db; form = header.form

# print search results
if form.has_key('query_string'):
	terms = header.re.findall("[\w]+",form['query_string'].value)
	sql = "SELECT documents.id,documents.title,SUM(document_tfs.frequency) AS tfs FROM document_tfs,documents WHERE "
	sql += "term=\"" + header.string.join(terms,"\" OR term=\"") + "\" " 
	sql += "AND doc_id=documents.id GROUP BY documents.title  ORDER BY `tfs` DESC LIMIT 30"
	db.execute(sql)
	print "<div id='search_results'><h3><span id='label'>results for</span>", form['query_string'].value, "</h3>"
	print "<ul>"
	for d_id,title,score in db.fetchall():
		print "<li><a href='document.py?id=" + str(d_id) + "'>" + title + "</a></li>"
	print "</ul>"
	print "<div class='clear'>&nbsp;</div></div>"

# print browse features and a little hello note.
else:
	
	print "<p>Search for an article above or browse below. This is a demo of a <a href='about.py'>semantic similarity algorithm</a>."
	
	alphalinks = "<div class='alphalinks'>\n"
	for letter in list(header.string.uppercase):
 		alphalinks += "<a href='?letter=" + letter + "'>" + letter + "</a> "
 	alphalinks += "</div>\n"

	print alphalinks
	
	if form.has_key('letter'):
		print "<div id='search_results'><h3>" + form['letter'].value + "</h3><ul>"
		sql = "SELECT id,title FROM documents WHERE title LIKE \"" + form['letter'].value + "%\" ORDER BY title ASC"
		db.execute(sql)
		for doc_id,title in db:
			print "<li><a href='document.py?id=" + str(doc_id) + "'>" + title + "</a></li>"
		print "</div>"
		
		print alphalinks
			
	
	
""" get a list of all the documents and print links """
#db.execute("SELECT id,title FROM documents ORDER BY title ASC")
#for row in db:
#	print "<a href='document.py?id=" + str(row[0]) + "'>" + row[1] + "</a><br>"


print header.footer


