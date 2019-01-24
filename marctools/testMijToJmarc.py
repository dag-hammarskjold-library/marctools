from pymongo import MongoClient
import json
from pymarcer import make_json, mijToJmarc

'''
mc=MongoClient()
db=mc['undlFiles']
ac=db["authRecords"]
bc=db["bibRecords"]
'''
if __name__ == '__main__':
    with open('jmarcDND.txt') as f, open('mijb.txt','w+') as f1, open('jmarcb.txt','w+') as f2:  
        #load jMarc json from a file
        dictJson = json.load(f)

        #get the JMarc json in mij format
        strMij=make_json(dictJson)
        f1.write(strMij)

        dictMij=json.loads(strMij)
        #get the jMarc from the mij format
        strJmarc1 = mijToJmarc(dictMij)
        f2.write(strJmarc1)