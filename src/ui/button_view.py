import disnake
from ui.modals import CardModal, DeckModal

class AddDeckButtonView(disnake.ui.View):

    def __init__(self, batch_id):
        super().__init__(timeout=300.0)
        self.batch_id = batch_id

        # Bouton d'ajout de decks
        self.add_deck_button=disnake.ui.Button(label = "Ajouter un Deck", row = 1, style=disnake.ButtonStyle.green, disabled = False)
        self.add_deck_button.callback=self.add_deck_callback
        self.add_item(self.add_deck_button)
        
    # Définition des callback des élément graphiques

    async def add_deck_callback(self, interaction: disnake.MessageInteraction):
        """Création d'un nouveau deck 

        Parameters
        ---------- 
        """
        deck_modal = DeckModal(interaction_id = interaction.id, batch_id = self.batch_id)
        await interaction.response.send_modal( modal = deck_modal)

class AddCardButtonView(disnake.ui.View):

    def __init__(self, deck_id):
        super().__init__(timeout=300.0)
        self.deck_id = deck_id

        # Bouton d'affichage d'information
        self.add_deck_button=disnake.ui.Button(label = "Ajouter une Carte Question", row = 1, style=disnake.ButtonStyle.green, disabled = False)
        self.add_deck_button.callback=self.add_deck_callback
        self.add_item(self.add_deck_button)
        
    # Définition des callback des élément graphiques

    async def add_deck_callback(self, interaction: disnake.MessageInteraction):
        """Création d'une nouvelle Carte question 

        Parameters
        ---------- 
        """
        deck_modal = CardModal(interaction_id = interaction.id, deck_id = self.deck_id)
        await interaction.response.send_modal( modal = deck_modal)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

        