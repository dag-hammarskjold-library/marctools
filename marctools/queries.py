'''

'''

from bson import SON

def match_subfield_value(tag,code,val):
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

