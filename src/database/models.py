from peewee import *

db = SqliteDatabase(None)

class BaseModel(Model):
    class Meta:
        database = db

class Servers(BaseModel):
    id = IntegerField(primary_key=True)
    server_name = CharField()
    study_channel = TextField()

class Decks(BaseModel):
    id = AutoField()
    server_id = ForeignKeyField(Servers, to_field=id)
    deck_name = CharField()
    is_updated = BooleanField(default = True)
    user_in_charge = CharField()

class Cards(BaseModel):
    id = AutoField()
    deck_id = ForeignKeyField(Decks, to_field=id)
    card_name = CharField()
    first_field = TextField()
    second_field = TextField() 
    is_active = BooleanField(default = True)