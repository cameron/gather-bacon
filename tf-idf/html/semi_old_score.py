#! /home/shanxi/opt/bin/python


import header; db = header.db_conn.db; form = header.cgi.FieldStorage()
import re,math



# list of document ids that don't already exist in 2 rows (one as doc1, another as doc2)
db.execute("SELECT id FROM documents")
db.execute("SELECT doc1,count FROM (SELECT doc1,COUNT(doc1) AS count FROM scores GROUP BY doc1) AS t1 WHERE count <" + str(db.rowcount-1)+";")
ids = [x[0] for x in db.fetchall()]

counter = 0


# get all the values 

# matrix row
for doc1 in ids:
	
	start_row = time.time() # start processing time for row of the scoring matrix
	
	db.execute("SELECT term,tfidf FROM document_tfs WHERE doc_id=%s",doc1)
	d1_terms = dict([(term,tfidf) for term,tfidf in db.fetchall()])
	
	# get list of ids to score against (by subtraction)
	db.execute("SELECT doc2 FROM scores WHERE doc1=%s",doc1)
	row_ids = ids.remove([x[0] for x in db.fetchall()])
	
	# process them in chunks to reduce sql queries
	segment = .1 # percentage
	iterations = round(1/segment)
	num_segment_ids = len(row_ids) / iterations
	for x in range(0,iterations):
		seg_ids = row_ids[x:num_segment_ids*(x+1)]
		for seg_id in seg_ids:
			
	
	# matrix cell
	for doc2 in ids:
		
		print "\tScoring doc", doc1, "against", doc2, ":"
		start_cell = time.time()
		
		
		start_sql = time.time()
		
		counter += 1
		
		
		
		start_terms_sql = time.time()
		
		db.execute("SELECT term,tfidf FROM document_tfs WHERE doc_id=%s",(doc2))		
		
		time_terms_sql = time.time() - start_terms_sql
		print "\t\tFetching terms took", round(time_terms_sql,7), "seconds"
		
		
		start_terms_sort = time.time()
		
		#d2_terms = dict([(term,tfidf) for term,tfidf in db.fetchall()])
		d2_terms = {}
		for term,tfidf in db:
			d2_terms[term] = tfidf
		
		
		time_terms_sort = time.time() - start_terms_sort
		print "\t\tSorting terms took", round(time_terms_sort,7), "seconds"
		
		
		
		start_euc = time.time()
		
		#euclidean distance
		s1 = s2 = float(0)
		for term,tfidf in d1_terms.iteritems():
			s1 += tfidf
		for term,tfidf in d2_terms.iteritems():
			s2 += tfidf
			
		euc_dist = math.sqrt(s1)*math.sqrt(s2)
		
		time_euc = time.time() - start_euc
		print "\t\tEuclidean distance took", round(time_euc,7), "seconds"
		
		
		
		start_dp = time.time()
		
		# dot product
		dp = float(0)
		term_set = set(d1_terms.keys()).intersection(set(d2_terms.keys()))
		for term in term_set:
			dp += d1_terms[term]*d2_terms[term]
		
		score = dp/euc_dist
		
		time_dp = time.time() - start_dp
		print "\t\tDot product took", round(time_dp,7), "seconds"
		
		
		
		start_insert = time.time()
		
		db.execute("INSERT INTO scores (doc1,doc2,score) VALUES (" + str(doc1) + "," + str(doc2) + "," + str(score) + "),(" + str(doc2) + "," + str(doc1) + "," + str(score) + ");")
		
		time_insert = time.time() - start_insert
		print "\t\tInsert took:",round(time_insert,7),"seconds"
		
		time_cell = time.time() - start_cell
		print "\t\tScoring time:", round(time_cell,7)
		print "\t\tPercentages:"
		print "\t\t\tScore check:", round(time_sql/time_cell,2)
		print "\t\t\tTerms sql:", round(time_terms_sql/time_cell,2), " (# terms : ",len(d2_terms), ")"
		print "\t\t\tTerms Sort:", round(time_terms_sort/time_cell,2)
		print "\t\t\tEuclidean Dist:", round(time_euc/time_cell,2)
		print "\t\t\tDot Product:", round(time_dp/time_cell,2)
		print "\t\t\tInsert:", round(time_insert/time_cell,2)
		
		
		
	print "Scored", counter, "documents against document", doc1, "in", str(round(time.time() - start_row,2)), "seconds"
	counter = 0