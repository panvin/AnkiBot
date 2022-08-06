from peewee import *

class dbManager():

    def __init__(self, database, path):
        # self.db = database
        # self.db.init(path)
        database.init(path)
        self.db = database

    def connect(self):
        self.db.connect(reuse_if_open=True)

    def close(self):
        self.db.close()