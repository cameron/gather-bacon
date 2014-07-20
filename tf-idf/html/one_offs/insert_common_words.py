#! /home/shanxi/opt/bin/python


import db_conn; db = db_conn.db; 


common_words = set([x[:-1] for x in open("../stoplist.txt").readlines() if x[0] != "#"])


for word in common_words:
	db.execute("INSERT INTO common_words (word) VALUES (\"" + word + "\");")