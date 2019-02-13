'''
'''

from pymongo import MongoClient

class DB(object):
	def __init__(self,connect_str):
		client = MongoClient(connect_str)
		self.db = client['undlFiles']
		self.auths = self.db['auth_JMARC']
		self.bibs = self.db['bib_JMARC']
		self.files = self.db['files']
		
	