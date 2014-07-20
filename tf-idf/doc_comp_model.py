#! /usr/bin/env python

# File: doc_comp_model.py
#
# Description: Experiments in semantic document comparison.
#
# This library consists of two (highly coupled) classes: Corpus and Document.
#
# Corpus
# Contains a list of Documents, a master Document (concatenation of all contained Docs)
# methods for adding new Documents, and methods for calculating the inverse document 
# frequencies (idf) of each term in the set of combined Document terms.
#
# Document
# Contains a Document string, a list of contained terms and methods for adding/subtracting 
# terms/strings/other Documents


import os,re,math
from operator import itemgetter
from decimal import *
from time import time

import wiki_parse
import xml.sax

# words to omit during term-based document comparison
common_words = set([x[:-1] for x in open("stoplist.txt").readlines() if x[0] != "#"])
		
class Document(object):
			
	def __init__(self,title="",content=""):
		
		self.title = str(title)
		self.raw_string = str(content)
		self.word_count = 0
		self.term_counts = {}				# (term,count) pairs				
		self.tfs = {}						# (term,tf) pairs. tf (term frequency) differs from count in that it is normalized to doc length

		self += self.raw_string
	
	def __add__(self,string): 

		if len(string) == 0:
			return
	
		word_list = self.clean_list_from_string(string)	

		# update self.term_counts and self.word_count
		for term in set(word_list):
			count = word_list.count(term)
			self.term_counts[term] = self.term_counts.get(term,0) + count
			self.word_count += count
		
		# update term frequencies
		for term,count in self.term_counts.items():
			self.tfs[term] = Decimal(count) / Decimal(self.word_count)
				
		return self
		
	
	def __iter__(self):
		for term,tf in self.tfs.items():
			yield (term,tf)
	
	
	# returns 0 for nonexistant terms
	def __getitem__(self,term):
		return self.tfs.get(str(term),0)
	
	
	def __str__(self):
		return self.raw_string
	
		
	def iterterms(self):
		for term in self.tfs.keys():
			yield term
	
	
	def terms(self):
		return self.tfs.keys()
	
	
	# returns list of forced-lowercase words minus:
	#		the set of common words
	# 		strings that are not words (according the regex character class: \w)
	def clean_list_from_string(self,string):
		return [x for x in re.sub("[^\w]+"," ",string.lower()).split() if len(x) > 1 and x not in common_words]	


######################
# End Document Class #

	
		
		
class Corpus(object):
	

	def __init__(self,path="",docs={}):
		
		self.chunk_length = 8000 # characters
		
		self.documents = {}					# (title,Document()) pairs
		self.dfs = {}						# (term,count) pairs, where count represents the number of documents in which a word appears
		self.idfs = {}						# (term,idf) pairs, where idf is the inverse document frequency of the given term 
		
		self.scoring_matrix = {}			# scoring_matrix[doc1.title][doc2.title] gives the latest computed similarity
											# measure between the given documents
											# (same value as scoring_matrix[doc2.title][doc1.title])
		
		
		# create the corpus!
		
		# if txt files found in "path" are longer in characters than self.chunk_length (defined above),
		# split them into self.chunk_length-sized strings and create documents with the results.
		# otherwise, just create one document per txt file.
		
		if len(path) != 0:
			path = path.rstrip("/")
			for file in [x for x in os.listdir(path) if x[-3:] == "txt"]:
				string = open(path + "/" + file).read()
				if len(string) > self.chunk_length:
					suffix = 0
					for chunk in self.chunk_string(string,self.chunk_length):
						self += Document(file + str(suffix),chunk)
						suffix += 1
				else:
					self += Document(file,string)
		
		
		# docs should be a dictionary of (title,text) pairs ready to be made into documents
		
		if len(docs) !=0:
			for title,text in docs.iteritems():
				self += Document(title,text)
			
		self.update_idfs()	
		self.score()
			
	
	# add a document to the corpus instance with the + or += operator	
	def __add__(self,doc):
		
		if(type(doc) is not type(Document(""))):
			raise TypeError, "Attempting to add non-Document() instance to Corpus() instance."
			
		self.documents[doc.title] = doc
	
		for term in doc.iterterms():
			self.dfs[term] = self.dfs.get(term,0) + 1
		
		return self
	
			
	# update the inverse document frequencies based on the self.dfs dictionary
	def update_idfs(self):
		num_docs = Decimal(len(self.documents))
		for term,dfs in self.dfs.iteritems():
			self.idfs[term] = Decimal(str(math.log(num_docs / Decimal(self.dfs[term]))))
	
	
	def __iter__(self):
		for title,doc in self.documents.iteritems():
			yield doc


	def __getitem__(self,index):
		return self.documents[int(index)]
	
	
	def __len__(self):
		return len(self.documents)
	
	
	def idf(self,term):
		return self.idfs[term]
	
	
	# split string into chunks of size chunk_length; returns a list of chunked strings		
	def chunk_string(self,string,chunk_length):  
		return [string[i*chunk_length:(i+1)*chunk_length] for i in range(int(math.ceil(len(string)/float(chunk_length))))]
	
	
	def euclidean_distance(self,doc1,doc2):
		term_set = set(doc1.terms()).union(set(doc2.terms()))
		s = 0
		for term in term_set:
			n = (doc1[term] - doc2[term])
			s += n*n # order of magnitude faster than pow(n,2)
	
		return Decimal(str(math.sqrt(s)))
	
	
	# roughly 25% faster than above... verify that they are mathematically equivalent
	def euclidean_distance2(self,doc1,doc2):
		s1 = 0
		s2 = 0
		for term,tf in doc1:
			s1 += tf*tf
		for term,tf in doc2:
			s2 += tf*tf
			
		return Decimal(str(math.sqrt(s1)*math.sqrt(s2)))

	
	def cosine_similarity(self,doc1,doc2):
		term_set = set(doc1.terms()).intersection(set(doc2.terms()))
		numer = Decimal(0)
		for term in term_set:
			w1 = doc1[term]*self.idfs[term]
			w2 = doc2[term]*self.idfs[term]
			numer += w1*w2
		denom = self.euclidean_distance2(doc1,doc2)
		
		if denom == 0:	# indicates identical documents
			numer = 1
			denom = 1
		
		return numer / denom
		
	
	def reset_scoring_matrix(self):
		self.scoring_matrix = {}
		for title in self.documents.keys():
			self.scoring_matrix[title] = dict([(x,None) for x in self.documents.keys()])
	
	def score(self):
		
		self.reset_scoring_matrix()
		
		print "Now scoring", len(self), "documents."
		
		
		for doc1 in self:
			
			start_time = time()
			
			for doc2 in self:

				# make sure we haven't already computed the score
				if self.scoring_matrix[doc1.title][doc2.title] == None: 
					print ".",
					score = self.cosine_similarity(doc1,doc2)

					self.scoring_matrix[doc1.title][doc2.title] = self.scoring_matrix[doc2.title][doc1.title] = score	
				


			print " time elapsed: ", (time() - start_time), "seconds"


	# returns list of (title,score) pairs of documents in descending order of similarity, up to num, or all if num is not specified
	def top_hits(self,doctitle,num=None):
		return sorted(self.scoring_matrix[doctitle].items(),key=itemgetter(1),reverse=True)[:num]	
			
			
	# similar to top_hits, but for a doc's individual terms
	def top_terms(self,doctitle,num=None):
		weights = {}
		for term,tf in self.documents[doctitle]:
			weights[term] = tf*self.idfs[term]
		
		return sorted(weights.items(),key=itemgetter(1),reverse=True)[:num]
	
	
if __name__ == "__main__":
	
	#corp = Corpus("../corpus")
	
	parser = xml.sax.make_parser()
	handler = wiki_parse.PageHandler(100)
	parser.setContentHandler(handler)
	
	# try..except structure necessary when 
	try:
		parser.parse("enwiki-20081008-pages-articles.xml")
	except:
		pass
	
	corp = Corpus(docs=handler.pages)
	
	
	
	print "Top terms by document"
	for doc in corp:
		print doc.title
		for term,weight in corp.top_terms(doc.title,15):
			print "\t" + str(term) + "\t\t" + str(round(weight,4))
		print 
	print "\n"
	
	print "Top matches by document"
	for doc in corp:
		print doc.title
		for title,score in corp.top_hits(doc.title,10):
			print "\t" + str(title) + "\t\t" + str(round(score,4))
		print
	print "\n"
	
