#! /home/shanxi/opt/bin/python


import header; db = header.db_conn.db; form = header.cgi.FieldStorage()
import re,math

# clear all tfs and corpus_word_count rows
db.execute("TRUNCATE tfs2")

# get common words
db.execute("SELECT word FROM common_terms")
common_words = []
for word in db:
	common_words.append(word)


total_docs = 2541

# update all tfs
counter = 1
db.execute("SELECT * FROM documents LIMIT 5")
for doc_id,title,body in db:
	print "Doc", counter, "of", total_docs
	counter += 1
	words = [x for x in re.sub("[^\w]+"," ",body.lower()).split() if len(x) > 1 and x not in common_words]
	length = len(words)
	word_counts = {}
	
	for word in set(words):
		word_counts[word] = word_counts.get(word,0) + words.count(word)
	
	# make a list of (doc_id,word,frequency) triplets that can be inserted as rows
	sql_values = []
	for word,count in word_counts.iteritems():
		sql_values.append((doc_id,word.encode('utf8','replace'),(float(count)/length)))

	db.executemany("INSERT INTO tfs2 (doc_id,term,frequency) VALUES (%s,%s,%s)",sql_values)
	
	