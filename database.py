from logger import Logger
from pymongo import MongoClient

class Database:
    def __init__(self, url, port, db_name, coll_name):
        self.url = url
        self.port = port
        self.db_name = db_name
        self.coll_name = coll_name
        self.connection = self.connect()
        self.log = Logger(type(self).__name__).log

    def get_collection(self):
        last_id = 0
        collection = self.connection[self.db_name][self.coll_name]
        if self.db_name in self.connection.database_names():
            self.log('Database exists.')
            if self.coll_name in db.collection_names():
                self.log('Collection exists, getting last id.')
            else:
                self.log('Collection doesn\'t exist but database does, last_id is staying 0.')
        else:
            self.log('Database doesn\'t exist, last_id is staying 0.')
        return (collection, last_id)

    def connect(self):
        return MongoClient(self.url, self.port)
