import disnake
from views.dropdown import CardDropdown
from views.modals import CardModal
from database.query import Query

class CardManagementView(disnake.ui.View):
    message: disnake.Message

    def __init__(self, deck_id, card_list):
        super().__init__(timeout=30.0)
        self.card_list=card_list
        self.deck_id=deck_id
        
        ########################## Première Ligne

        # Menu déroulant contenant les cartes questions
        self.card_dropdown=CardDropdown(row = 1, is_disabled = False, card_list=card_list)
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
        deck_modal = CardModal(interaction_id = interaction.id, deck_id = self.deck_id)
        await interaction.response.send_modal( modal = deck_modal)
    
    async def show_card_callback(self, interaction: disnake.MessageInteraction):

        await interaction.response.edit_message("**Affichage des informations:** ", view=self)
    
    
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

    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

        