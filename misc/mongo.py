import os

from pymongo import MongoClient


def connect(db, collection):
    client = MongoClient(
        os.environ['MONGODB_HOST'],
        int(os.environ['MONGODB_PORT']),
    )
    output = client[db][collection]
    return output


mongoDB = connect
