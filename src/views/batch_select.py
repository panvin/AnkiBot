import disnake
from views.deck_select import DeckSelectView
from views.dropdown import BatchDropdown
from views.modals import  DeckModal
from database.query import Query

class BatchSelectView(disnake.ui.View):
    message: disnake.Message

    def __init__(self, batch_list):
        super().__init__(timeout=300.0)
        self.query = Query()
        self.batches_list=batch_list
        
        ########################## Première Ligne
        
        # Menu déroulant contenant les decks
        self.batch_dropdown=BatchDropdown(row = 1, is_disabled = False, batch_list = batch_list)
        self.batch_dropdown.callback=self.select_batch_callback
        self.add_item(self.batch_dropdown)

        ########################## Seconde Ligne
        
        # Bouton d'ajout de promotions
        self.add_deck_batch_button=disnake.ui.Button(label = "Ajouter un Deck", row = 2, style=disnake.ButtonStyle.green, disabled = True)
        self.add_deck_batch_button.callback=self.add_deck_batch_callback
        self.add_item(self.add_deck_batch_button)

        # Bouton d'ajout de promotions
        self.add_card_batch_button=disnake.ui.Button(label = "Ajouter une Carte", row = 2, style=disnake.ButtonStyle.green, disabled = True)
        self.add_card_batch_button.callback=self.add_card_batch_callback
        self.add_item(self.add_card_batch_button)
        
    # Définition des callback des élément graphiques

    async def select_batch_callback(self, interaction: disnake.MessageInteraction):

        self.add_deck_batch_button.disabled = False
        self.add_card_batch_button.disabled = False
        for option in self.batch_dropdown.options:
            if option.value == interaction.values[0]:
                option.default = True
            else:
                option.default = False
        await interaction.response.edit_message("**Création:** ", view=self)

    async def add_deck_batch_callback(self, interaction: disnake.MessageInteraction):
        """Ajout d'une carte dans la promotion sélectionné

        Parameters
        ---------- 
        """
        batch_id = self.batch_dropdown.values[0]
        deck_modal = DeckModal(interaction_id = interaction.id, batch_id = batch_id)
        await interaction.response.send_modal( modal = deck_modal)
        #supression du message initial ou mise à jour de la liste de batch

    async def add_card_batch_callback(self, interaction: disnake.MessageInteraction):
        """Selection d'un élement de la liste pour passer à la suite

        Parameters
        ---------- 
        """
        batch_id = self.batch_dropdown.values[0]
        decks_list = self.query.get_decks_list_from_batch(batch_id)
        deck_view = DeckSelectView(decks_list)
        await interaction.response.edit_message("Création: ", view = deck_view, ephemeral = True)



    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

        