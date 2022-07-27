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
    def get_decks_list(self,id):
        deck_list =  Decks.select().where(Decks.server_id==id)
        return deck_list

    @connection_wrapper
    def get_deck_by_id(self,id):
        deck =  Decks.get(id=id)
        return deck

    @connection_wrapper
    def get_card_list(self,id):
        card_list =  Cards.get_by_id(id)
        return card_list

    @connection_wrapper
    def create_card(self, deck_id, card_name, first_field, second_field):
        card = Cards.create(deck_id = deck_id, card_name=card_name, first_field=first_field, second_field=second_field)
        return card

    @connection_wrapper
    def create_deck(self, server_id, deck_name):
        deck = Decks.create(server_id = server_id, deck_name=deck_name)
        return deck

    @connection_wrapper
    def create_server(self, server_id, server_name):
        server = Servers.create(id=server_id, server_name = server_name)
        return server
    