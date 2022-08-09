import disnake
from ui.anki_embed import AnkiEmbed
from ui.batch_select_view import BatchSelectView
from ui.deck_select_view import DeckSelectView
from ui.dropdown_view import DropDownView
from ui.modals import CardModal

class CardManagementView(DropDownView):

    def __init__(self, cards_list):
        placeholder = "Choix de la Carte question"
        super().__init__(timeout=300.0, fn_select_option = self.card_select_option, placeholder = placeholder, item_list = cards_list)

        ########################## Seconde Ligne

        # Bouton d'ajout de cartes
        self.add_card_button=disnake.ui.Button(label = "Ajouter", row = 2, style=disnake.ButtonStyle.green, disabled = False)
        self.add_card_button.callback=self.add_card_callback
        self.add_item(self.add_card_button)
        
        # Bouton d'affichage d'information
        self.show_card_button=disnake.ui.Button(label = "Infos", row = 2, style=disnake.ButtonStyle.primary, disabled = True)
        self.show_card_button.callback=self.show_card_callback
        self.add_item(self.show_card_button)
        
        # Bouton d'affichage de modification
        self.update_card_button=disnake.ui.Button(label = "Modifier", row = 2, style=disnake.ButtonStyle.primary, disabled = True)
        self.update_card_button.callback=self.update_card_callback
        self.add_item(self.update_card_button)

        # Bouton de suppression
        self.delete_card_button=disnake.ui.Button(label = "Supprimer", row = 2, style=disnake.ButtonStyle.red, disabled = True)
        self.delete_card_button.callback=self.delete_card_callback
        self.add_item(self.delete_card_button)

    # Définition des callback des élément graphiques

    async def select_callback(self, interaction: disnake.MessageInteraction):

        if interaction.values[0] == "+" or interaction.values[0] == "-":
            self.show_card_button.disabled   = True
            self.update_card_button.disabled = True
            self.delete_card_button.disabled = True
        else:
            self.show_card_button.disabled   = False
            self.update_card_button.disabled = False
            self.delete_card_button.disabled = False
        super().select_callback(interaction = interaction)
        await interaction.response.edit_message("**Gestion des Cartes:** ", view=self)

    async def add_card_callback(self, interaction: disnake.MessageInteraction):
        """Création d'un nouveau deck 

        Parameters
        ---------- 
        """
        # Construction de la liste de promotion et de deck à partiur des cartes dans la view
        batches_list = []
        decks_list = [] 
        for card in self.item_list:
            if card.deck is not None and card.deck not in decks_list:
                decks_list.append(card.deck)
                if card.deck.batch_id is not None and card.deck.batch not in batches_list:
                    batches_list.append(card.deck.batch)

        if batches_list is None or len(batches_list) == 0:
            await interaction.response.send_message(" Vous n'êtes membre d'aucune promotion", ephemeral=True)
        elif len(batches_list) == 1 and len(decks_list) == 1:
            deck =   decks_list[0]
            card_modal = CardModal(interaction_id = interaction.id, deck_id = deck.id)  
            await interaction.response.send_modal( modal = card_modal)
        elif len(batches_list) == 1 and len(decks_list) > 1:
            deck_view = DeckSelectView(decks_list)
            await interaction.response.edit_message( "Création:" , view = deck_view)
        else:
            batch_view = BatchSelectView(batches_list)
            await interaction.response.edit_message( "Création:" , view = batch_view)
    
    async def show_card_callback(self, interaction: disnake.MessageInteraction):

        """Affichage d'informations et de commandes relatives à la Carte question affichée 

        Parameters
        ---------- 
        """
        choosen_card = None
        for card in self.item_list:
            if card.id == int(self.item_dropdown.values[0]):
                choosen_card = card
                break

        if choosen_card is not None:
            embed = AnkiEmbed().card_embed(choosen_card)
        await interaction.send(embed = embed, ephemeral=True)
    
    async def update_card_callback(self, interaction: disnake.MessageInteraction):
        """Mise à jour du nom du Deck 

        Parameters
        ---------- 
        """
        selected_card_id=int(self.item_dropdown.values[0])
        card = self.query.get_card_by_id(selected_card_id)
        card_modal = CardModal(interaction_id = interaction.id, deck_id = card.deck_id, card = card)
        await interaction.response.send_modal( modal = card_modal)
        #supression du message initial ou mise à jour de la liste de batch

    async def delete_card_callback(self, interaction: disnake.MessageInteraction):

        await interaction.send("Suppression en cours", ephemeral=True)

    def get_available_batches(self, member : disnake.Member):
        #On récupère les identifiants de roles
        role_id = []
        for role in member.roles:
            role_id.append(role.id)
        return self.query.get_batches_from_roles(role_list = role_id)

    def card_select_option(self, card):
        return disnake.SelectOption(
                    label = card.card_name,
                    description = f"Deck: {card.deck.deck_name}",
                    value = str(card.id)
                )      