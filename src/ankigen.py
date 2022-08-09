import os
from posixpath import basename
import sys
import genanki
from database.query import Query
from settings import output_path
from zipfile import ZipFile

class AnkiGenerator():

    def __init__(self, decks_list = None) -> None:
        self.decks_list = decks_list
        self.query = Query()
        self.anki_dict = {}
        self.deck_dict = {}

        self.model = genanki.Model(
        1607392319,
        'Simple Model',
        fields=[
            {'name': 'CName'},
            {'name': 'Question'},
            {'name': 'Answer'},
        ],
        templates=[
            {
            'name': '{{CName}}',
            'qfmt': '{{Question}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
            },
            {
            'name': '{{CName}}',
            'qfmt': '{{Answer}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Question}}',
            },
        ])

    def generate_deck(self):
        for deck in self.decks_list:

            anki_deck = genanki.Deck(deck_id = hash(deck.deck_name), name = deck.deck_name, description = deck.deck_name)
            cards_list = self.query.get_cards_list(deck.id)

            if len(cards_list) == 0:
                continue

            for card in cards_list:
               note = genanki.Note(model=self.model, fields=[card.card_name, card.first_field, card.second_field]) 
               anki_deck.add_note(note)
            
            file_name = f"{deck.id}_{deck.deck_name}.apkg".replace(' ', '_')
            # self.anki_decks[file_name] = [deck, anki_deck]
            self.deck_dict[file_name] = deck
            self.anki_dict[file_name] = anki_deck

    def generate_files(self):
        for file_name, anki in self.anki_dict.items():
            deck = self.deck_dict.get(file_name, None)
            full_name = os.path.join(output_path, file_name)
            try:
                genanki.Package(anki).write_to_file(full_name)
                self.query.update_deck_state(deck.id)
            except :
                print("Unexpected error: ", sys.exc_info[0])

class BatchGenerator():
    def __init__(self, batch_id_list) -> None:
        self.batch_id_list = batch_id_list
        self.query = Query()


    def generate_batch_archive(self):
        
        for batch_id in self.batch_id_list:
            files_names = []

            deck_list = self.query.get_decks_list_from_batch(batch_id)

            if deck_list is None:
                print("Erreur, deck list en erreur")
            if deck_list is not None and len(deck_list) == 0:
                continue

            for deck in deck_list:
                card_count = self.query.count_cards_in_decks(deck.id)
                if card_count == 0:
                    continue

                batch_name = deck.batch.batch_name
                batch_id = deck.batch_id
                package_name = f"{deck.id}_{deck.deck_name}.apkg".replace(' ', '_')
                full_name = os.path.join(output_path, package_name)
                files_names.append(full_name)

            zip_name = f"{batch_id}_{batch_name}.zip".replace(' ', '_')
            full_zip_name = os.path.join(output_path, zip_name)
            zip_obj = ZipFile(full_zip_name, 'w')

            for name in files_names:
                zip_obj.write(name, basename(name))
            zip_obj.close()


