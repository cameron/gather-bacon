#! /usr/bin/env python

import MySQLdb

conn = MySQLdb.connect(host="localhost",
                       user="shanxi",
                       passwd="tknpitoz",
                       db="exs_dcm")				
db = conn.cursor()
