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
import re
import pymongo
from pymongo import MongoClient
from bson.son import SON

class DLX(object):
	def __init__(self,connect_str):
		client = MongoClient(connect_str)
		self.db = client['undlFiles']
		self.auths = self.db['auth_JMARC']
		self.bibs = self.db['bib_JMARC']
		self.files = self.db['files']

class Subfield(object):
	def __init__(self,sub):
		self.code = sub['code']
		self.value = sub['value']
	
class Controlfield(object):
	def __init__(self,field):
		self.tag = field['tag']
		self.value = field['value']
	
class Datafield(object):
	def __init__(self,field):
		self.tag = field['tag']
		self.ind1 = field['ind1']
		self.ind2 = field['ind2']
		self.subfield = list(map(lambda x: Subfield(x), field['subfield']))
		
	def get_value(self,code):
		for sub in self.subfield:
			if sub.code == code:
				return sub.value

	def get_values(self,*codes):
		ret_vals = []
		
		for sub in self.subfield:
			if sub.code in codes:
				ret_vals.append(sub.value)
		
		return ret_vals
		
class JMARC(object):
	def __init__(self,doc):
		self.id = doc['_id']
		self.leader = doc['leader']
		self.controlfield = list(map(lambda x: Controlfield(x), doc['controlfield']))
		self.datafield = list(map(lambda x: Datafield(x), doc['datafield']))
		
	def get_fields(self,tag):
		return filter(lambda x: True if x.tag == tag else False, self.datafield)
		
	def get_field(self,tag):
		return next(self.get_fields(tag), None)
		
	def get_value(self,tag,code):
		# returns the first value found
		
		field = self.get_field(tag)
		
		if field.__class__.__name__ == 'Controlfield':
			return field.value
		
		return field.get_value(code)

	def get_values(self,tag,*codes):
		# returns list of values
	
		ret_vals = []
		
		for field in self.get_fields(tag):
			vals = field.get_values(*codes)
			if not vals:
				pass
			else:
				ret_vals.append(field.get_values(*codes))
		
		# this is the onyl way to flatten a list in python?? 😕
		return [x for y in ret_vals for x in y]
		
####

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
	print(list(jmarc.get_values('245','a','b','c')))
	
####
	
main()