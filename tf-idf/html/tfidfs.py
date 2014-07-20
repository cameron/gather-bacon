#! /home/shanxi/opt/bin/python


import header; db = header.db_conn.db; form = header.cgi.FieldStorage()
import re,math

# reset tfidf
#db.execute("UPDATE document_tfs SET tfidf=0")

# get total document count
db.execute("SELECT COUNT(*) FROM documents")
row = db.fetchone()
total_docs = row[0]

print "Total docs:", total_docs

# get a list of terms and idfs
idfs = {}
db.execute("SELECT term,LOG10(" + str(total_docs) +"/COUNT(term)) FROM document_tfs GROUP BY term;")
for term,idf in db:
	idfs[term] = idf
	
# update the tfidf field for each document-term (do this by document to avoid memory issues)
db.execute("SELECT DISTINCT id FROM documents;")
for doc_id in db:
	doc_id = doc_id[0]
	print "Updating tfidfs for document #", doc_id
	db.execute("SELECT term,frequency FROM document_tfs WHERE doc_id=\"" + str(doc_id) + "\";")
	tfidfs = {}
	for term,tf in db:
		tfidfs[term] = tf*idfs[term]
	tfidfs = [(tfidf,term,doc_id) for tfidf,term in zip(tfidfs.values(),tfidfs.keys())]
	#db.executemany("""UPDATE document_tfs SET tfidf=\"%s\" WHERE term=\"%s\" AND doc_id=\"%s\";""",tfidfs)
	for tfidf,term,doc_id in tfidfs:
		sql = "UPDATE document_tfs SET tfidf=%s WHERE term=\"%s\" AND doc_id=\"%s\";" % (tfidf,term,doc_id)
		db.execute(sql)		