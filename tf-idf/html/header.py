#! /usr/bin/env python

import db_conn; db = db_conn.db

import cgi; form  = cgi.FieldStorage();
import cgitb; cgitb.enable() # for debugging

import re,math,string


print """
<html>
<head>
<title>Semantic Document Comparison Playground</title>

<link rel="stylesheet" href="css/base.css" type="text/css">

<script type='text/javascript'>

	// actions for clearing default form field

</script>

</head>
<body>
<div id='top_nav'>
	<div id='search'>
		<form id='search_form' action='index.py' method='GET'>
			<input type='text' name='query_string' size='20' default='Search for an article'> <input type='submit' name='search' value='Search'>
		</form>
		<a id='browse' href='index.py'>Browse</a> | <em>This site is the product of a <a href='about.py'>semantic similarity algorithm</a> and 2541 Wikipedia articles.</em>
	</div>
</div>
<div id='page'>
"""

footer = """
</div>
</body>
</html>"""
