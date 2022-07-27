
from database.query import Query
from settings import db_path

# rec1 = Servers.create(id = 1235, server_name = "Le serveur des canards", study_channel = "Channel1234")

# rec2 = Decks.create(id = 1, server_id = 1234, deck_name = "Deck name", is_updated = True, user_in_charge = "Vincent")

# rec3 = Cards.create(id = 1, deck_id = 1, card_name = "Card name", first_field = "Question", second_field = "Reponse", is_active = True)

#rec = Servers.get_by_id(1235)
#rec.server_name = "Le serveur des ours"
#rec.save()
#print(rec.server_name)

query = Query(db_path)

deck_list = query.get_decksList(1234)
print(deck_list.deck_name)

