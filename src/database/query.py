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
            ret = func(*args, **kwargs)
            args[0].manager.close()
            return ret    
        return function_wrapper

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
    def get_batch_by_id(self,id: int):
        batch =  Batches.get_by_id(id)
        return batch

    @connection_wrapper
    def update_batch_manager(self, batch_id: int, manager: int):
        query = Batches.update(batch_manager=manager).where(Batches.id == batch_id)
        return query.execute()

    @connection_wrapper
    def update_batch_member(self, batch_id: int, member: int):
        query = Batches.update(batch_member=member).where(Batches.id == batch_id)
        return query.execute()

    @connection_wrapper
    def update_batch_name(self, batch_id: int, name: str):
        query = Batches.update(batch_name=name).where(Batches.id == batch_id)
        return query.execute()
    
    @connection_wrapper
    def get_batches_from_roles(self, role_list : list[int]):
        batches_list = Batches.select().where(Batches.batch_member << role_list)
        return batches_list

    @connection_wrapper
    def count_decks_in_batches(self, batch_id: int):
        return Decks.select().where(Decks.batch_id == batch_id).count()

    ######################################################
    #                 Decks Queries                      #
    ######################################################

    @connection_wrapper
    def create_deck(self, batch_id: int, deck_name: str, manager:str = None):
        deck = Decks.create(batch_id = batch_id, deck_name=deck_name, deck_manager=manager)
        return deck

    @connection_wrapper
    def get_decks_list_from_batch(self,id : int):
        decks_list =  list(Decks.select().where(Decks.batch_id==id))
        return decks_list


    @connection_wrapper
    def get_deck_by_id(self, id: int):
        deck =  Decks.get_by_id(id)
        return deck

    @connection_wrapper
    def get_deck_or_none(self, id: int):
        deck =  Decks.get_or_none(Decks.id == id)
        return deck

    @connection_wrapper
    def update_deck_manager(self, deck_id: int, manager: str):
        query = Decks.update(deck_manager = manager).where(Decks.id == deck_id)
        return query.execute()

    @connection_wrapper
    def update_deck_name(self, deck_id: int, name: str):
        query = Decks.update(deck_name=name, is_updated=True).where(Decks.id == deck_id)
        return query.execute()

    @connection_wrapper
    def update_deck_state(self, deck_id: int):
        query = Decks.update(is_updated=False).where(Decks.id == deck_id)
        return query.execute()

    @connection_wrapper
    def get_decks_from_roles(self, role_list : list[int]):
        decks_list = Decks.select().join(Batches, on=(Decks.batch_id == Batches.id)).where(Batches.batch_member << role_list)
        return decks_list

    @connection_wrapper
    def get_decks_to_update(self):
        decks_list = Decks.select().where(Decks.is_updated == True)
        return decks_list

    @connection_wrapper
    def count_cards_in_decks(self, deck_id: int):
        return Cards.select().where(Cards.deck_id == deck_id).count()
    
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

    @connection_wrapper
    def update_card_fields(self, card_id: int, name: str, first_field: str, second_field: str):
        number_of_row_updated = 0
        card = Cards.get_or_none(card_id)
        query = Cards.update(card_name = name, first_field = first_field, second_field = second_field).where(Cards.id == card_id).execute()
        number_of_row_updated += query
        query = Decks.update(is_updated = True).where(Decks.id == card.deck_id).execute()
        number_of_row_updated += query
        return number_of_row_updated

    @connection_wrapper
    def get_card_by_id(self, id: int):
        card =  Cards.get_by_id(id)
        return card

    @connection_wrapper
    def get_cards_from_roles(self, role_list : list[int]):
        subquery = Decks.select().join(Batches, on=(Decks.batch_id == Batches.id)).where(Batches.batch_member << role_list)
        card_list = Cards.select().join(subquery, on=Cards.deck_id == subquery.c.id)
        return card_list