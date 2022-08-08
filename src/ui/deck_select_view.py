import disnake
from database.query import Query
from ui.deck_view import DeckView
from ui.modals import CardModal

class DeckSelectView(DeckView):

    def __init__(self, decks_list):
        super().__init__(timeout=300.0, decks_list = decks_list)

        ########################## Seconde Ligne

        # Bouton d'affichage d'information
        self.add_card_button=disnake.ui.Button(label = "Ajouter", row = 2, style=disnake.ButtonStyle.green, disabled = True)
        self.add_card_button.callback=self.add_card_callback
        self.add_item(self.add_card_button)

    # Définition des callback des élément graphiques

    async def select_deck_callback(self, interaction: disnake.MessageInteraction):
        self.add_card_button.disabled   = False
        super().select_deck_callback(interaction = interaction)
        await interaction.response.edit_message("**Création:** ", view=self)

    async def add_card_callback(self, interaction: disnake.MessageInteraction):
        """Création d'une nouvelle carte 

        Parameters
        ---------- 
        """
        selected_deck = self.deck_dropdown.values[0]
        card_modal = CardModal(interaction_id=interaction.id, deck_id = selected_deck) 
        await interaction.response.send_modal( modal = card_modal)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

        