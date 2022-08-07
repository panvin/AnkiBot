import disnake
from database.query import Query

class BatchModal(disnake.ui.Modal):
    
    def __init__(self, interaction_id, batch = None):
        self.batch = batch
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
            Query().create_batch(server_id = guild_id, name = name, manager = default_manager, member = default_member, channel = default_channel, delay = delay)
            await inter.response.send_message("Nouvelle promotion crée")

        else:
            batch_id = self.batch.id
            Query().update_batch_name(batch_id = batch_id, name = name)
            await inter.response.send_message("Nom de la promotion mis à jour")

        

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
            Query().create_deck(batch_id = parent_batch_id, deck_name = name, manager = default_manager)
            await inter.response.send_message("Nouveau deck crée")

        else:
            deck_id = self.deck.id
            Query().update_deck_name(deck_id = deck_id, name = name)
            await inter.response.send_message("Nom du deck mis à jour")

        

#    async def on_error(self, error: Exception, inter: disnake.ModalInteraction):
#        await inter.response.send_message(f"An error occurred!\n```{error}```")

class CardModal(disnake.ui.Modal):
    
    def __init__(self, interaction_id, deck_id :int, card = None):
        self.card = card
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
            Query().create_card(deck_id = parent_deck_id, card_name = name, first_field = first_field, second_field = second_field)
            await inter.response.send_message("Nouvelle Carte question créée")

        else:
            card_id = self.card.id
            
            Query().update_card_fields(card_id = card_id, name = name, first_field = first_field, second_field = second_field)
            await inter.response.send_message("Carte mise à jour", ephemeral = True)

        

#    async def on_error(self, error: Exception, inter: disnake.ModalInteraction):
#        await inter.response.send_message(f"An error occurred!\n```{error}```")
