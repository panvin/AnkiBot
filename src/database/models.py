from peewee import *

db = SqliteDatabase(None, pragmas={'foreign_keys': 1})

class BaseModel(Model):
    class Meta:
        database = db

class Batches(BaseModel):
    id = AutoField()
    server_id = IntegerField()
    batch_name = CharField()
    batch_manager = IntegerField()
    batch_member = IntegerField()
    study_channel = IntegerField()
    delay = IntegerField(default = 240)

class Decks(BaseModel):
    id = AutoField()
    batch = ForeignKeyField(model=Batches)
    deck_name = CharField()
    is_updated = BooleanField(default = True)
    deck_manager = IntegerField()

class Cards(BaseModel):
    id = AutoField()
    deck = ForeignKeyField(model=Decks)
    card_name = CharField()
    first_field = TextField()
    second_field = TextField() 