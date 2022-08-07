import disnake
from views.dropdown import DeckDropdown
from database.query import Query
from views.modals import CardModal

class DeckSelectView(disnake.ui.View):

    def __init__(self, decks_list):
        super().__init__(timeout=300.0)
        self.query = Query()
        self.decks_list=decks_list
        
        ########################## Première Ligne
        
        # Menu déroulant contenant les decks
        self.deck_dropdown=DeckDropdown(row = 1, is_disabled = False, deck_list = decks_list)
        self.deck_dropdown.callback=self.select_deck_callback
        self.add_item(self.deck_dropdown)

        ########################## Seconde Ligne

        # Bouton d'affichage d'information
        self.add_card_button=disnake.ui.Button(label = "Ajouter", row = 2, style=disnake.ButtonStyle.green, disabled = True)
        self.add_card_button.callback=self.add_card_callback
        self.add_item(self.add_card_button)

    # Définition des callback des élément graphiques

    async def select_deck_callback(self, interaction: disnake.MessageInteraction):
        self.add_card_button.disabled   = False
    
        for option in self.deck_dropdown.options:
            if option.value == interaction.values[0]:
                option.default = True
            else:
                option.default = False

        await interaction.response.edit_message("**Gestion des decks:** ", view=self)

    async def add_card_callback(self, interaction: disnake.MessageInteraction):
        """Création d'une nouvelle carte 

        Parameters
        ---------- 
        """
        selected_deck = self.deck_dropdown.values[0]
        card_modal = CardModal(interaction_id=interaction.id, deck_id = selected_deck) 
        await interaction.response.send_modal( modal = card_modal)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

        