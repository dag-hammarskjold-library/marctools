#!/usr/bin/env python

'''
Usage: 

python jmarc.py <MongoDB connection string> <tag> <subfield code> <value to match>
i.e. -> python jmarc.py "mongodb://..." 191 a S/2011/10
'''

import sys
'''
sys.path holds the dirs that Python looks in to find modules to load. sys.path[0] holds.
sys.path[0] is the directory the script is run from. 
'''
sys.path[0] = sys.path[0] + '\..'

from marctools.jmarc import JMARC
from marctools.dlx import DB
from marctools.queries import *

#import .marctools

def test(jmarc):
	# prints title
	print('Title: ' + ' '.join(jmarc.get_values('245','a','b','c')))
	
	print('\n')
	
	# prints the JMARC object seraliazed as json (unordered keys)
	print(jmarc.to_json())
	
	print('\n')
	
	# prints json serliazation in MIJ format
	print(jmarc.to_mij())
	
	print('\n')
	
	# prints the BSON serialization (oredered keys) suitable for inserting into DLX (MongoDB)  
	print(jmarc.to_bson())
	
	print('\n')
	
	# convert to a pymarc object
	pymarc_record = jmarc.to_pymarc()
	
	# looks like pymarc record objects serialize to .mrk by default
	print(pymarc_record)
	
	# prints marc21 in utf8 (because its in utf8 in DLX)
	# 	how to print as marc8??? 
	print(pymarc_record.as_marc21())
		

def run():
	connect_str = sys.argv[1]
	tag = sys.argv[2]
	code = sys.argv[3]
	val = sys.argv[4]
	
	print(connect_str)
	
	db = DB(connect_str)
	
	query = match_subfield_value(tag,code,val)
	
	cursor = db.bibs.find(query)
	
	if cursor is None:
		print('no results :(')
		return
	
	for doc in cursor:
		jmarc = JMARC(doc)
	
		print(jmarc.get_value('001'))

	
####
	
run()