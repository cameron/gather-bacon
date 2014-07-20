#! /home/shanxi/opt/bin/python

import header; db = header.db_conn.db; form = header.cgi.FieldStorage()
import re,math

#fresh start
db.execute("TRUNCATE corpus_word_counts")


# get doc count
db.execute("SELECT COUNT(*) FROM corpus")
row = db.fetchone()
total = row[0]

# get tf row count
db.execute("SELECT COUNT(*) FROM tfs")
row = db.fetchone()
tf_count = row[0]

# loop through all tf rows
terms = {}
limit = 10000
rows = 0

while rows < tf_count:
	print "Processing rows", rows, "through", rows + limit, "of", tf_count
	db.execute("SELECT doc_id,term FROM tfs LIMIT " + str(limit) + " OFFSET " + str(rows))
	for doc_id,term in db:
		terms[term] = terms.get(term,0) + 1
	
	rows += limit
	

term_counts = [] # (term,count) tuples for sql insertion
for term,count in terms.iteritems():
	term_counts.append((term,count))


db.executemany("INSERT INTO corpus_word_counts (term,count) VALUES (%s,%s)", term_counts)	


