
import sqlite3
from time import sleep
from database.query import Query
from settings import test_guild
import random
import string

query = Query()

# deck_list = query.get_decksList(1234)
#query.create_server(test_guild, "Test serveurs")

S = 10  # number of characters in the string.  

#for i in [0,1,2,3,4,5]:
#    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))
    # deck = query.create_deck(test_guild, deck_name=ran)
#    try:
#        deck = query.create_deck(batch_id = 2, deck_name=ran)
#        for i in [0,1,2,3]:
#            try:
#                ran2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))
#                query.create_card(deck.id, ran2, "Question", "Réponse ")
#                sleep(1)
#            except sqlite3.IntegrityError as err:
#                print(f"Erreur Foreign Key pour le deck_id = {deck.id+1}")
#        sleep(1)
#    except sqlite3.IntegrityError as err:
#        print(f"Erreur Foreign Key pour le batch_id = 2")
"""
print("Liste des batches")
batches = query.get_batches_from_roles([1004066091590496322])
for batch in batches:
    print (f"{batch.id}\t{batch.batch_name}")

print("\nListe des decks")
decks = query.get_decks_from_roles([1004066091590496322])
for deck in decks:
    print (f"{deck.id}\t{deck.batch_id}\t{deck.deck_name}")

print("\nListe des cartes")
cards = query.get_cards_from_roles([1004066091590496322])
for card in cards:
    print (f"{card.id}\t{card.deck_id}\t{card.card_name}")

dict = {14:2, 16:23}
dict = None
dict.get(14)
"""

first = [i for i in range(1,50)]
option_list = []
if(len(first) > 25):
    chunk = first[0:24] + ['suivant...']
    option_list.append(chunk)
    i = 24
    while len(first) - i > 23:
        chunk = ['précédent...'] + first[i:i+23] + ['suivant...']
        option_list.append(chunk)
        i = i+23
    chunk = ['précédent...'] + first[i:]
    option_list.append(chunk)
else:
    option_list.append(first)

print(option_list)