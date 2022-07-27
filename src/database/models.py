from peewee import *

db = SqliteDatabase(None)

class BaseModel(Model):
    class Meta:
        database = db

class Servers(BaseModel):
    id = PrimaryKeyField()
    server_name = CharField()
    study_channel = TextField()

class Decks(BaseModel):
    id = PrimaryKeyField()
    server_id = ForeignKeyField(Servers, field=Servers.id)
    deck_name = CharField()
    is_updated = BooleanField(default = True)
    user_in_charge = CharField()

class Cards(BaseModel):
    id = PrimaryKeyField()
    deck_id = ForeignKeyField(Decks, field=Decks.id)
    card_name = CharField()
    first_field = TextField()
    second_field = TextField() 
    is_active = BooleanField(default = True)