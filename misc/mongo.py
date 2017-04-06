from pymongo import MongoClient

def connect(db, collection):
    client = MongoClient('140.112.147.132')
    client.admin.authenticate('achiii', 'gjoKClmg8eQDF4pKeVXMkTnX7wL/9MVilkavArDouNA=')
    output = client[db][collection]
    return output

mongoDB = connect #"connect" in PTTCorp is equivalent to "mongoDB" in COPENS

# This is used for accessing mongodb without authentication
#from pymongo import Connection
#def connect(db, collection):
#	C = Connection(host='localhost', port=27017)
#	output = C[db][collection]
#	C.close()
#	return output
