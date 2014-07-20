#! /usr/bin/env python

import MySQLdb

conn = MySQLdb.connect(		host = "dcm.exsupera.com",
							user = "exsupera",
							passwd = "tknpitoz",
							db = "exs_dcm")				
db = conn.cursor()
