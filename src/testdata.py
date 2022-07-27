
from time import sleep
from database.query import Query
from settings import db_path
from settings import test_guild
import random
import string

query = Query(db_path)

# deck_list = query.get_decksList(1234)
query.create_server(test_guild, "Test serveurs")

S = 10  # number of characters in the string.  

for i in [0,1,2,3,4,5]:
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))
    deck = query.create_deck(test_guild, deck_name=ran)
    for i in [0,1,2,3]:
        ran2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))
        query.create_card(deck.id+1, ran2, "Question", "Réponse ")
        sleep(1)
    sleep(1)