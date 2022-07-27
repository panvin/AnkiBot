from .models import *
from .db_manager import dbManager

class Query:

    def __init__(self, db_path):
        self.manager = dbManager( db, db_path)

    def connection_wrapper(func):
        def function_wrapper(*args, **kwargs):
            args[0].manager.connect()
            func(*args, **kwargs)
            args[0].manager.close()
            return function_wrapper
        return func

    @connection_wrapper
    def get_decksList(self,id):
        deck_list =  Decks.get(server_id=id)
        return deck_list

    @connection_wrapper
    def get_deck(self,id):
        deck =  Decks.get(id=id)
        return deck

    @connection_wrapper
    def get_decksList(self,id):
        deck_list =  Decks.get(server_id=id)
        return deck_list

    @connection_wrapper
    def get_decksList(self,id):
        deck_list =  Decks.get(server_id=id)
        return deck_list

    @connection_wrapper
    def get_decksList(self,id):
        deck_list =  Decks.get(server_id=id)
        return deck_list
    
    