import disnake
from database.query import Query
from ui.anki_embed import AnkiEmbed

class BatchModal(disnake.ui.Modal):
    
    def __init__(self, interaction_id, batch = None):
        self.batch = batch
        self.query = Query()
        self.batch_custom_id = f"batch-modal-{interaction_id}"
        if batch is None:
            initial_value = None
        else:
            initial_value = batch.batch_name
        
        components = [
                disnake.ui.TextInput(
                    label = "Nom: ",
                    placeholder = "Le nom de la promotion à créer ou à modifier",
                    custom_id = "batch-name",
                    style = disnake.TextInputStyle.short,
                    min_length = 3,
                    max_length = 100,
                    value = initial_value 
                )
            ]

        super().__init__(
            title="Ajout/Modification",
            custom_id=self.batch_custom_id,
            components=components,
            timeout=300
            )

    async def callback(self, inter: disnake.ModalInteraction):
        name = inter.text_values.get("batch-name")
        if self.batch is None:
            guild_id = inter.guild_id
            default_manager = None
            default_member = inter.guild_id
            default_channel = self.get_authorized_channel(inter.guild)
            delay = None
            batch = self.query.create_batch(server_id = guild_id, name = name, manager = default_manager, member = default_member, channel = default_channel, delay = delay)
            deck_count = 0
            embed = AnkiEmbed().batch_embed(guild = inter.guild , batch = batch, deck_count = deck_count)
            await inter.response.send_message("Nouvelle Promotion créée", embed = embed, ephemeral = True)

        else:
            batch_id = self.batch.id
            batch = self.query.update_batch_name(batch_id = batch_id, name = name)
            deck_count = self.query.count_decks_in_batches(batch_id = batch.id)
            embed = AnkiEmbed().batch_embed(guild = inter.guild , batch = batch, deck_count = deck_count)
            await inter.response.send_message("Promotion mise à jour", embed = embed, ephemeral = True) 

#    async def on_error(self, error: Exception, inter: disnake.ModalInteraction):
#        await inter.response.send_message(f"An error occurred!\n```{error}```")

    def get_authorized_channel(self, guild : disnake.Guild):
        channel_id = None
        for channel in guild.text_channels: 
            if channel.permissions_for(guild.me).send_messages:
                channel_id = channel.id
                break 
        return channel_id

class DeckModal(disnake.ui.Modal):
    
    def __init__(self, interaction_id, batch_id :int, deck = None):
        self.deck = deck
        self.query = Query()
        self.batch_id = batch_id
        self.deck_custom_id = f"deck-modal-{interaction_id}"
        if deck is None:
            initial_value = None
        else:
            initial_value = deck.deck_name
        
        components = [
                disnake.ui.TextInput(
                    label = "Nom: ",
                    placeholder = "Le nom du deck à créer ou à modifier",
                    custom_id = "deck-name",
                    style = disnake.TextInputStyle.short,
                    min_length = 3,
                    max_length = 100,
                    value = initial_value 
                )
            ]

        super().__init__(
            title="Ajout/Modification",
            custom_id=self.deck_custom_id,
            components=components,
            timeout=300
            )

    async def callback(self, inter: disnake.ModalInteraction):
        name = inter.text_values.get("deck-name")
        if self.deck is None:
            parent_batch_id = self.batch_id
            default_manager = None
            deck = self.query.create_deck(batch_id = parent_batch_id, deck_name = name, manager = default_manager)
            card_count = 0
            embed = AnkiEmbed().deck_embed(guild = inter.guild, deck = deck, card_count = card_count)
            await inter.response.send_message("Nouveau Deck crée", embed = embed, ephemeral = True)

        else:
            deck_id = self.deck.id
            deck = self.query.update_deck_name(deck_id = deck_id, name = name)
            card_count = self.query.count_cards_in_decks(deck_id = deck.id)
            embed = AnkiEmbed().deck_embed(guild = inter.guild, deck = deck, card_count = card_count)
            await inter.response.send_message("Deck mis à jour", embed = embed, ephemeral = True)

#    async def on_error(self, error: Exception, inter: disnake.ModalInteraction):
#        await inter.response.send_message(f"An error occurred!\n```{error}```")

class CardModal(disnake.ui.Modal):
    
    def __init__(self, interaction_id, deck_id :int, card = None):
        self.card = card
        self.query = Query()
        self.deck_id = deck_id
        self.card_custom_id = f"card-modal-{interaction_id}"
        if card is None:
            initial_name         = None
            initial_first_value  = None
            initial_second_value = None
        else:
            initial_name         = card.card_name
            initial_first_value  = card.first_field
            initial_second_value = card.second_field
        
        components = [
                disnake.ui.TextInput(
                    label = "Nom: ",
                    placeholder = "Le nom de la carte question à créer ou à modifier",
                    custom_id = "card-name",
                    style = disnake.TextInputStyle.short,
                    min_length = 3,
                    max_length = 100,
                    value = initial_name 
                ),
                disnake.ui.TextInput(
                    label="Question: ",
                    placeholder="Les champs question et réponse doivent être interchangeables",
                    custom_id="card-first-field",
                    style=disnake.TextInputStyle.paragraph,
                    min_length=3,
                    max_length=4000,
                    value = initial_first_value
                ),
                disnake.ui.TextInput(
                    label="Réponse: ",
                    placeholder="Les champs question et réponse doivent être interchangeables",
                    custom_id="card-second-field",
                    style=disnake.TextInputStyle.paragraph,
                    min_length=3,
                    max_length=4000,
                    value = initial_second_value
                )
            ]

        super().__init__(
            title="Ajout/Modification",
            custom_id=self.card_custom_id,
            components=components,
            timeout=300
            )

    async def callback(self, inter: disnake.ModalInteraction):
        name = inter.text_values.get("card-name")
        first_field = inter.text_values.get("card-first-field")
        second_field = inter.text_values.get("card-second-field")

        if self.card is None:
            parent_deck_id = self.deck_id
            card = self.query.create_card(deck_id = parent_deck_id, card_name = name, first_field = first_field, second_field = second_field)
            embed = AnkiEmbed().card_embed(card = card)
            await inter.response.send_message("Nouvelle Carte question créée", embed = embed, ephemeral = True)

        else:
            card_id = self.card.id
            
            card = self.query.update_card_fields(card_id = card_id, name = name, first_field = first_field, second_field = second_field)
            embed = AnkiEmbed().card_embed(card = card)
            await inter.response.send_message("Carte mise à jour", embed = embed, ephemeral = True)

#    async def on_error(self, error: Exception, inter: disnake.ModalInteraction):
#        await inter.response.send_message(f"An error occurred!\n```{error}```")