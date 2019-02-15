

'''

'''

import json
from bson.son import SON
from pymarc import JSONReader



class Subfield(object):
	def __init__(self,sub):
		self.code = sub['code']
		self.value = sub['value']

	def to_bson(self):
		return SON(data = {'code' : self.code, 'value' : self.value})

class Controlfield(object):
	def __init__(self,field):
		self.tag = field['tag']
		self.value = field['value']

	def to_bson(self):
		return SON(data = {'tag' : self.tag, 'value' : self.value})
	
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
		
	def to_bson(self):
		return SON (
			data = {
				'tag' : self.tag,
				'ind1' : self.ind1,
				'ind2' : self.ind2,
				'subfield' : list(map(lambda x: x.to_bson(), self.subfield))
			}
		)
	
class JMARC(object):
	def __init__(self,doc):
		self.id = doc['_id']
		self.leader = doc['leader']
		# not sure why list comprehensions don't work here 
		#self.controlfield = [Controlfield(x) for x in doc['controlfield']]
		#self.datafield = [Datafield(x) for x in doc['controlfield']]
		self.controlfield = list(map(lambda x: Controlfield(x), doc['controlfield']))
		self.datafield = list(map(lambda x: Datafield(x), doc['datafield']))

	# accessors
	
	def get_fields(self, tag = None):
		if tag is None:
			return self.controlfield + self.datafield
		return filter(lambda x: True if x.tag == tag else False, self.controlfield + self.datafield)
		
	def get_field(self,tag):
		return next(self.get_fields(tag), None)
		
	def get_value(self,tag,code = None):
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
		
		# this is the only way to flatten a list in python?? 😕
		return [x for y in ret_vals for x in y]
		
	def tags(self):
		# trying list comprehension instead of map
		return [x.tag for x in self.get_fields()]
	
	# utlities 
	
	def diff(self,jmarc):
		pass
	
	# serializations
	
	def to_bson(self):
		return SON (
			data = {
				'_id' : self.id,
				'leader' : self.leader,
				'controlfield' : list(map(lambda x: x.to_bson(), self.controlfield)),
				'datafield' : list(map(lambda x: x.to_bson(), self.datafield))
			}
		)
	
	def to_dict(self):
		return self.to_bson().to_dict()
		
	def to_json(self):
		return json.dumps(self.to_dict())
	
	def to_mij(self):
		mij = {}
		mij['leader'] = self.leader	
		fields = []
		
		for f in self.controlfield:
			fields.append({f.tag : f.value})
		
		for f in self.datafield:
			fields.append(
				{
					f.tag : {
						'subfields' : list(map(lambda x: {x.code : x.value}, f.subfield)),
						'ind1' : f.ind1,
						'ind2' : f.ind2,
					}
				}
			)
		
		mij['fields'] = fields
		
		return json.dumps(mij)
				
	def to_pymarc(self):
		reader = JSONReader(self.to_mij())
		
		for r in reader:
			r.force_utf8 = True
			return r

