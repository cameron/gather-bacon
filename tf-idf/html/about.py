#! /usr/bin/env python
print "Content-type: text/html\r\n\r\n"

	
import header; db = header.db; form = header.form

print """
<div id='about'>
<h2>What Is This Site?</h2>
<p>This site is a demonstration of a semantic similarity algorithm performing on a test corpus of selected Wikipedia articles.<br/><br/>As part of my senior design project at Santa Clara University, <a href='#author'>I</a>'m developing a system that will provide users of my team's note-taking web interface with links to related note documents. For example, if you're taking notes on the Works Progress Administration, my algorithm should provide you with links to other users' notes on the Great Depression, FDR, unemployment, and perhaps WWII.<br/><br/>This site is simply a demonstration of the algorithm that will be implemented in the final project.</p>

<h2>The Algorithm</h2>
<p>I opted for the <a href='http://en.wikipedia.org/wiki/Tf-idf'>tf-idf</a> weighting scheme, a <a href='http://en.wikipedia.org/wiki/Vector_space_model'>vector space</a> model, and the <a href='http://en.wikipedia.org/wiki/Cosine_similarity'>cosine similarity</a> measure, a tried-and-true combination from the field of <a href='http://en.wikipedia.org/wiki/Information_retrieval'>Information Retrieval</a>. (IR applcations include context-appropriate advertising, such as Google's AdSense, though I can't say for sure that Google takes the same approach.)<br/><br/>To sum up the contents of the pages linked to above, the algorithm represents each document in the corpus (the corpus being the collection of all documents concerned) as a vector with one component for each unique word in the corpus. Each vector component is the product of two word-specific statistics: term frequency and inverse document frequency (hence tf-idf). Term frequency is the number of occurences of a word, for example, "dirigible", in the document (the doc for which we are constructing a vector) divided by the total number of words in the same document. Inverse document frequency is the total number of documents in the corpus divided by the number of documents in which the word "dirigible" appears. Put another way, the vector component representing "dirigible" (or any word) will be a relatively high value if it occurs frequently in our present document and exists in a small number of other documents across the entire corpus.<br/><br/>Once the vectors are constructed, dividing the dot product of any two vectors by the product of their magnitudes gives the angle between them (this is the cosine similarity formula). The smaller the angle between the vectors, the more closely related are the documents which they represent.</p>


<h2>The Corpus</h2>
<p>The corpus is a selection of 2541 Wikipedia articles that I found on the blog of <a href='http://evanjones.ca/software/wikipedia2text.html'>Evan Jones</a>. I did a pretty hacky job of cleaning out all the markup, but this is just a proof of concept, and the algorithm seems not to mind much. If you're interested in extracting data from Wikipedia for computational, informational, or recreational purposes, <a href='http://meta.wikimedia.org/wiki/Special:Export'>check this out</a>.</p>

<h2 id='author'>The Author</h2>
<p>My name is Cameron Boehmer, and I'm a senior at Santa Clara University graduating June 2009 with a B.S. in computer engineering. You can find more of my work at <a href="http://cameronboehmer.com/">cameronboehmer.com</a>.</p>
</div>
</div>
"""

print header.footer


