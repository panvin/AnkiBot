import disnake
from views.batch_select import BatchSelectView
from views.deck_select import DeckSelectView
from views.dropdown import CardDropdown
from views.modals import CardModal
from database.query import Query

class CardManagementView(disnake.ui.View):
    message: disnake.Message

    def __init__(self, cards_list):
        super().__init__(timeout=300.0)
        self.query = Query()
        self.cards_list = cards_list
        
        ########################## Première Ligne

        # Menu déroulant contenant les cartes questions
        self.card_dropdown=CardDropdown(row = 1, is_disabled = False, cards_list=cards_list)
        self.card_dropdown.callback=self.select_card_callback
        self.add_item(self.card_dropdown)

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

    async def select_card_callback(self, interaction: disnake.MessageInteraction):

        self.show_card_button.disabled   = False
        self.update_card_button.disabled = False
        self.delete_card_button.disabled = False
        for option in self.card_dropdown.options:
            if option.value == interaction.values[0]:
                option.default = True
            else:
                option.default = False
        await interaction.response.edit_message("**Gestion des Cartes:** ", view=self)

    async def add_card_callback(self, interaction: disnake.MessageInteraction):
        """Création d'un nouveau deck 

        Parameters
        ---------- 
        """
        # Construction de la liste de promotion et de deck à partiur des cartes dans la view
        batches_list = []
        decks_list = [] 
        for card in self.cards_list:
            if card.deck_id is not None and card.deck_id not in decks_list:
                decks_list.append(card.deck_id)
                if card.deck.batch_id is not None and card.deck.batch_id not in batches_list:
                    batches_list.append(card.deck.batch_id)

        if batches_list is None or len(batches_list) == 0:
            await interaction.response.send_message(" Vous n'êtes membre d'aucune promotion", ephemeral=True)
        elif len(batches_list) == 1 and len(decks_list) == 1:
            deck_id =   decks_list[0]
            card_modal = CardModal(interaction_id = interaction.id, deck_id = deck_id)  
            await interaction.response.send_modal( modal = card_modal)
        elif len(batches_list) == 1 and len(decks_list) > 1:
            deck_view = DeckSelectView(decks_list)
            await interaction.response.edit_message( "Création:" , view = deck_view)
        else:
            deck_view = BatchSelectView(batches_list)
            await interaction.response.edit_message( "Création:" , view = deck_view)
    
    async def show_card_callback(self, interaction: disnake.MessageInteraction):

        choosen_card = None
        for card in self.cards_list:
            if card.id == int(self.card_dropdown.values[0]):
                choosen_card = card
                break

        if choosen_card is not None:
            message = f"**Nom de la Carte:** {choosen_card.card_name} - **ID:** {choosen_card.id}\n**Nom du Deck:** {choosen_card.deck.deck_name} - **ID:** {choosen_card.deck_id}\n**Question: **{choosen_card.first_field}\n**Réponse:** {choosen_card.second_field}"
        else:
            message = "Une erreur s'est produit, impossible d'afficher les informations"
        await interaction.send(message, ephemeral=True)
    
    
    async def update_card_callback(self, interaction: disnake.MessageInteraction):
        """Mise à jour du nom du Deck 

        Parameters
        ---------- 
        """
        selected_card_id=int(self.card_dropdown.values[0])
        card = Query().get_card_by_id(selected_card_id)
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
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

        