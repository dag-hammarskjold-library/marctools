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

    # Some records had been missing 001, so I am checking and adding it if necessary
    try:
        this_001 = pymarc['fields']['001']
        pass
    except KeyError:
        pymarc['fields'].append({'001': jmarc['_id']})

    # Let's see if we can make json, then read that into pymarc
    pymarc_json = json.dumps(pymarc)
    return pymarc_json