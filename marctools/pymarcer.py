import json

def make_json(jmarc):
    pymarc = {}
    # The id field is unnecessary in a pymarc record
    #pymarc['_id'] = jmarc['_id']
    pymarc['leader'] = jmarc['leader']
    pymarc['fields'] = []



    # Process the controlfield entries
    for cf in jmarc['controlfield']:
        tag = cf['tag']
        val = cf['value']
        this_field = {}
        this_field[tag] = val
        pymarc['fields'].append(this_field)

    # Process datafield entries
    for df in jmarc['datafield']:
        tag = df['tag']
        ind1 = df['ind1']
        ind2 = df['ind2']
        this_field = {
            tag: {
                'subfields': [],
                'ind1': ind1,
                'ind2': ind2
            }
        }
        # Now process subfield entries
        for sf in df['subfield']:
            sf_code = sf['code']
            sf_val = sf['value']
            this_subfield = {}
            this_subfield[sf_code] = sf_val
            this_field[tag]['subfields'].append(this_subfield)
        pymarc['fields'].append(this_field)

    # Let's see if we can make json, then read that into pymarc
    pymarc_json = json.dumps(pymarc)
    return pymarc_json


    '''
mijToJmarc converts python dict from Marc-In-Json(mij) to JMarc format
if loaded from a json file; json.loads is assumed to have been executed to get -mij-

Type: Function
Argument: a python dict in mij format
Return value: a python dict in jmarc format
    '''
def mijToJmarc(mij):
    jMarc={}
    #jMarc["_id"]=mij["_id"]
    jMarc["leader"]=mij["leader"]
    jMarc["datafield"]=[]
    jMarc["controlfield"]=[]
    # top level array of fields in mij
    for field in mij["fields"]:
        tempDict={}
        #dictionary with a key tag
        #values is dictionary with keys 'subfields', ind1, ind2, tag
        for k,v in field.items():
            if k=="001":
                tempDict["tag"]=k
                tempDict["value"]=v
                jMarc["controlfield"].append(tempDict)
            elif k=="008":
                tempDict["tag"]=k
                tempDict["value"]=v
                jMarc["controlfield"].append(tempDict)
            else:
                #tempTag = k
                #capture a tag
                tempDict["tag"]=k
                tempSubfield=[]
                for i1 in v["ind1"]:
                    tempDict["ind1"]=v["ind1"]
                for i2 in v["ind2"]:
                    tempDict["ind2"]=v["ind2"]
                    #sf is a specific element in subfields array
                for sf in v["subfields"]:
                    #i,j are subfield code,value pairs respectively
                    for i,j in sf.items():
                        tagSubfield={"code":i, "value":j}
                        tempSubfield.append(tagSubfield)
                    tempDict["subfield"]=tempSubfield
                jMarc["datafield"].append(tempDict)
    "convert to string to return"
    strjMarc =json.dumps(jMarc)
    return strjMarc
