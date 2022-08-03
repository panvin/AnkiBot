from peewee import *

db = SqliteDatabase(None)

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
    batch_id = ForeignKeyField(Batches, to_field=id)
    deck_name = CharField()
    is_updated = BooleanField(default = True)
    deck_manager = IntegerField()

class Cards(BaseModel):
    id = AutoField()
    deck_id = ForeignKeyField(Decks, to_field=id)
    card_name = CharField()
    first_field = TextField()
    second_field = TextField() 