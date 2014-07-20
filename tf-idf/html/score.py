#! /home/shanxi/opt/bin/python


import header; db = header.db_conn.db; form = header.cgi.FieldStorage()
import re,math




# list of document ids that don't already exist in 2 rows (one as doc1, another as doc2)
db.execute("SELECT id FROM documents")
db.execute("SELECT doc1,count FROM (SELECT doc1,COUNT(doc1) AS count FROM scores GROUP BY doc1) AS t1 WHERE count <" + str(db.rowcount-1)+";")
ids = [x[0] for x in db.fetchall()]

counter = 0

# matrix row
for doc1 in ids:
	
	print "Scoring document", counter, "of", len(ids)
	counter += 1
	
	start_row = time.time() # start processing time for row of the scoring matrix
	
	# get terms for doc1
	db.execute("SELECT term,tfidf FROM document_tfs WHERE doc_id=%s",doc1)
	d1_terms = dict([(term,tfidf) for term,tfidf in db.fetchall()])
	
	# get list of ids to score against (by subtraction)
	db.execute("SELECT doc2 FROM scores WHERE doc1=%s",doc1) # assumes that all calculated scores exist as both (docX,docY) and (docY,docX)
	row_ids = list(set(ids) - set([x[0] for x in db.fetchall()]))
	
	# process them in chunks to reduce sql queries
	segment = .1 # percentage
	iterations = int(round(1/segment))
	num_segment_ids = int(math.ceil(len(row_ids) / iterations))
	
	print "Segment size:", num_segment_ids
	
	for x in range(0,iterations):
		print "\tStarting segment", x, "of", iterations, "row segments...",
	
		start_iter = start_iter_terms = time.time()
		
		seg_ids = row_ids[x:num_segment_ids*(x+1)]
		sql = "SELECT doc_id,term,tfidf FROM document_tfs WHERE doc_id=" + " OR doc_id=".join(map(str,seg_ids))
		db.execute(sql)
		doc_tfidfs = dict([(doc_id,{}) for doc_id in seg_ids]) #  of the form: {doc_id:{term:tfidf}} 
		for doc_id,term,tfidf in db:
			doc_tfidfs[doc_id][term] = tfidf	
		
		time_iter_terms = time.time() - start_iter_terms
		
		
		start_iter_score = time.time()
		error_count = 0
		
		for doc2 in doc_tfidfs:
			
			
			#print "\t\tDocument",doc1,"vs.",doc2
			
			start_euc = start_cell = time.time()
			
			d2_terms = doc_tfidfs[doc2]
			
		
			#euclidean distance
			s1 = s2 = float(0)
			for term,tfidf in d1_terms.iteritems():
				s1 += tfidf
			for term,tfidf in d2_terms.iteritems():
				s2 += tfidf
			
			euc_dist = math.sqrt(s1)*math.sqrt(s2)
		
			time_euc = time.time() - start_euc
			#print "\t\t\tEuclidean distance took", round(time_euc,7), "seconds"
		
		
		
			start_dp = time.time()
		
			# dot product
			dp = float(0)
			term_set = set(d1_terms.keys()).intersection(set(d2_terms.keys()))
			for term in term_set:
				dp += d1_terms[term]*d2_terms[term]
		
			score = dp/euc_dist
		
			time_dp = time.time() - start_dp
			#print "\t\t\tDot product took", round(time_dp,7), "seconds"
		
		
		
			start_insert = time.time()
			
			
			try:
				db.execute("INSERT INTO scores (doc1,doc2,score) VALUES (" + str(doc1) + "," + str(doc2) + "," + str(score) + "),(" + str(doc2) + "," + str(doc1) + "," + str(score) + ");")
			except db_conn.MySQLdb.IntegrityError,e:
				error_count += 1
			
			time_insert = time.time() - start_insert
			#print "\t\t\tInsert took:",round(time_insert,7),"seconds"
		
			time_cell = time.time() - start_cell
			#print "\t\t\tScoring time:", round(time_cell,7)
			#print "\t\t\tPercentages:"
			#print "\t\t\t\tEuclidean Dist:", round(time_euc/time_cell,2)
			#print "\t\t\t\tDot Product:", round(time_dp/time_cell,2)
			#print "\t\t\t\tInsert:", round(time_insert/time_cell,2)
		
		end_iter = time.time()
		time_iter_score = end_iter - start_iter_score
		time_iter = end_iter - start_iter
		print " finished in:", round(time_iter,2), "seconds with", error_count, "errors"
		print "\t\tPercent iter terms:", round(time_iter_terms / time_iter,2)
		print "\t\tPercent iter score:", round(time_iter_score / time_iter,2)
		
		
		
	print "Finished in", round(time.time() - start_row,2), "seconds"
	print