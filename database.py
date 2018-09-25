import json
from logger import Logger
from pymongo import MongoClient
from configparser import ConfigParser


class Database:
    def __init__(self, host, port, db_username, db_password, db_name, coll_name):
        self.host = host
        self.port = port
        self.username = db_username
        self.password = db_password
        self.db_name = db_name
        self.coll_name = coll_name
        self.connection = self.connect()
        self.log = Logger(type(self).__name__).log

        self.db = self.connection[db_name]
        self.collection = self.db[coll_name]

    def export_data(self):
        config = ConfigParser()
        config.read('config')
        data_file = config['Export']['DataFile']
        lines = None
        with open(data_file, 'r') as df:
            lines = df.readlines()

        if lines:
            for line in lines:
                current = json.loads(line)
                self.collection.insert_one(current)

    def connect(self):
        return MongoClient(('mongodb://%s:%s@' + self.host) % (self.username, self.password))
