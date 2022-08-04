import disnake
from views.dropdown import DeckDropdown
from database.query import Query
from views.modals import DeckModal
from views.card_management import CardManagementView

class DeckManagementView(disnake.ui.View):

    def __init__(self, batch_id, decks_list):
        super().__init__(timeout=30.0)
        self.decks_list=decks_list
        self.batch_id = batch_id
        
        ########################## Première Ligne
        
        # Menu déroulant contenant les decks
        self.deck_dropdown=DeckDropdown(row = 1, is_disabled = False, deck_list = decks_list)
        self.deck_dropdown.callback=self.select_deck_callback
        self.add_item(self.deck_dropdown)

        ########################## Seconde Ligne

        # Bouton d'affichage d'information
        self.add_deck_button=disnake.ui.Button(label = "Ajouter", row = 2, style=disnake.ButtonStyle.green, disabled = False)
        self.add_deck_button.callback=self.add_deck_callback
        self.add_item(self.add_deck_button)
        
        # Bouton d'affichage d'information
        self.show_deck_button=disnake.ui.Button(label = "Infos", row = 2, style=disnake.ButtonStyle.primary, disabled = True)
        self.show_deck_button.callback=self.show_deck_callback
        self.add_item(self.show_deck_button)

        # Bouton d'affichage d'information
        self.manage_card_button=disnake.ui.Button(label = "Cartes", row = 2, style=disnake.ButtonStyle.primary, disabled = True)
        self.manage_card_button.callback=self.manage_card_callback
        self.add_item(self.manage_card_button)
        
        # Bouton d'affichage de modification
        self.update_deck_button=disnake.ui.Button(label = "Modifier", row = 2, style=disnake.ButtonStyle.primary, disabled = True)
        self.update_deck_button.callback=self.update_deck_callback
        self.add_item(self.update_deck_button)

        # Bouton de suppression
        self.delete_deck_button=disnake.ui.Button(label = "Supprimer", row = 2, style=disnake.ButtonStyle.red, disabled = True)
        self.delete_deck_button.callback=self.delete_deck_callback
        self.add_item(self.delete_deck_button)

    # Définition des callback des élément graphiques

    async def select_deck_callback(self, interaction: disnake.MessageInteraction):
        self.show_deck_button.disabled   = False
        self.manage_card_button.disabled = False
        self.update_deck_button.disabled = False
        self.delete_deck_button.disabled = False
        
        for option in self.deck_dropdown.options:
            if option.value == interaction.values[0]:
                option.default = True
            else:
                option.default = False

        await interaction.response.edit_message("**Gestion des decks:** ", view=self)

    async def add_deck_callback(self, interaction: disnake.MessageInteraction):
        """Création d'un nouveau deck 

        Parameters
        ---------- 
        """
        deck_modal = DeckModal(interaction_id = interaction.id, batch_id = self.batch_id)
        await interaction.response.send_modal( modal = deck_modal)
        #supression du message initial ou mise à jour de la liste de decks

    async def show_deck_callback(self, interaction: disnake.MessageInteraction):
        await interaction.send(f"Affichage d'informations", ephemeral=True)

    async def manage_card_callback(self, interaction: disnake.MessageInteraction):
        selected_deck_id=int(self.deck_dropdown.values[0])
        card_list = Query().get_cards_list(selected_deck_id)
        
        if card_list is None or len(card_list) == 0: 
            await interaction.response.send_message("Le deck ne contient aucune carte", ephemeral = True)
        else:
            new_view = CardManagementView(selected_deck_id, card_list)
            await interaction.response.edit_message("**Gestion des Decks:** ", view=new_view)
    
    async def update_deck_callback(self, interaction: disnake.MessageInteraction):
        """Mise à jour du nom du Deck 

        Parameters
        ---------- 
        """
        selected_deck_id=int(self.deck_dropdown.values[0])
        deck = Query().get_deck_by_id(selected_deck_id)
        deck_modal = DeckModal(interaction_id = interaction.id, batch_id = deck.batch_id, deck = deck)
        # await interaction.response.send_modal( modal = deck_modal)
        #supression du message initial ou mise à jour de la liste de batch
        

        await interaction.send("Modification en cours", ephemeral=True)
        
    async def delete_deck_callback(self, interaction: disnake.MessageInteraction):

        await interaction.send("Suppression en cours", ephemeral=True)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

        