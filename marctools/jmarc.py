#!/usr/bin/env python

'''
This is a demo for working with raw JMARC data through a client. 
The DLX class jsut provides a shortcut for connectiong to the db. 
The JMARC class can provide methods for pulling data out of JMARC.
Implementations of classes like this would normally be in separate files, 
so that they can be resused as needed. 

See the main() function for the demo.

Usage for this script: 

python jmarc.py <MongoDB connection string> <tag> <subfield code> <value to match>
i.e. -> python jmarc.py "mongodb://..." 191 a S/2011/10
'''

import sys
import json 
import pymongo
from pymongo import MongoClient
from bson.son import SON

class DLX:
	def __init__(self,connect_str):
		client = MongoClient(connect_str)
		self.db = client['undlFiles']
		self.auths = self.db['auth_JMARC']
		self.bibs = self.db['bib_JMARC']
		self.files = self.db['files']
		
class JMARC:
	def __init__(self,doc):
		self.data = doc
			
	def get_fields(self,tag):
		return filter(lambda x: True if x.get('tag') == tag else False, self.data['datafield'])
		
	def get_value(self,tag,code):
		# returns the first value found
		
		df = next(self.get_fields(tag), None)
		
		for sub in df['subfield']:
			return sub['value']

	def get_values(self,tag,code):
		# returns list of values
		
		ret_vals = []
		
		for df in self.get_fields(tag):
			for sub in df['subfield']:
				ret_vals.append(sub['value'])
		
		return ret_vals

def match_subfield_value(tag,code,val):
	# this would normally be imported from a library of utilites
	return SON (
		data = {
			'datafield' : {
				'$elemMatch' : {
					'tag' : tag,
					'subfield' : {
						'code' : code,
						'value' : val
					}
				}
			}
		}
	)
		
def main():
	connect_str = sys.argv[1]
	tag = sys.argv[2]
	code = sys.argv[3]
	val = sys.argv[4]
	
	dlx = DLX(connect_str)
	
	query = match_subfield_value(tag,code,val)
	
	doc = dlx.bibs.find_one(query)
	
	if doc is None:
		print('no results :(')
		return
	
	jmarc = JMARC(doc)
	
	# prints title
	print(jmarc.get_value('245','a'))

####
	
main()
