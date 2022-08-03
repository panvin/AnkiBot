from .models import *
from .db_manager import dbManager
from settings import db_path

class Query:

    def __init__(self):
        self.manager = dbManager(db, db_path)

    ######################################################
    #               Connection Wrapper                   #
    ######################################################
    
    def connection_wrapper(func):
        def function_wrapper(*args, **kwargs):
            args[0].manager.connect()
            func(*args, **kwargs)
            args[0].manager.close()
            return function_wrapper
        return func

    ######################################################
    #                Batches Queries                     #
    ######################################################

    @connection_wrapper
    def create_batch(self, server_id :int, name :str, manager :int, member :int, channel :int, delay :int):
        batch = Batches.create( server_id=server_id, batch_name=name, batch_manager=manager, batch_member=member, study_channel=channel, delay=delay)
        return batch

    @connection_wrapper
    def is_default_batch_created(self, server_id):
        batch = Batches.get_or_none(Batches.server_id == server_id, Batches.batch_name == "default")
        if batch is None:
            return False
        else:
            return True

    @connection_wrapper
    def get_batches_list(self, server_id):
        batches_list =  list(Batches.select().where(Batches.server_id==server_id))
        return batches_list

    @connection_wrapper
    def get_default_batch(server_id):
        batch = Batches.get_or_none(Batches.server_id == server_id, Batches.batch_name == "default")
        return batch

    ######################################################
    #                 Decks Queries                      #
    ######################################################

    @connection_wrapper
    def create_deck(self, batch_id: int, deck_name: str, user_in_charge:str = None):
        deck = Decks.create(batch_id = batch_id, deck_name=deck_name, user_in_charge=user_in_charge)
        return deck
    
    @connection_wrapper
    def get_decks_list(self,id : int):
        decks_list =  list(Decks.select().join(Batches).where(Batches.server_id==id))
        return decks_list

    @connection_wrapper
    def get_decks_as_dictionnary(self,id : int):
        deck_list =  list(Decks.select().where(Decks.server_id==id))
        deck_dictionnary = {}
        for deck in deck_list:
            deck_dictionnary[deck.id]=deck.deck_name
        return deck_dictionnary


    @connection_wrapper
    def get_deck_by_id(self,id: int):
        deck =  Decks.get_by_id(id)
        return deck

    @connection_wrapper
    def update_deck_manager(self, deck_id: int, manager: str):
        query = Decks.update(user_in_charge=manager).where(Decks.id == deck_id)
        return query.execute()
    
    ######################################################
    #                   Cards Queris                     #
    ######################################################

    @connection_wrapper
    def create_card(self, deck_id, card_name, first_field, second_field):
        card = Cards.create(deck_id = deck_id, card_name=card_name, first_field=first_field, second_field=second_field)
        return card
    
    @connection_wrapper
    def get_cards_list(self, deck_id):
        card_list =  list(Cards.select().where(Cards.deck_id==deck_id))
        return card_list