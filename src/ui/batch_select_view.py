import disnake
from ui.deck_select_view import DeckSelectView
from ui.dropdown_view import DropDownView
from ui.modals import  DeckModal

class BatchSelectView(DropDownView):

    def __init__(self, batch_list):
        placeholder = "Choix de la Promotion"
        super().__init__(timeout=300.0, fn_select_option = self.batch_select_option, placeholder = placeholder, item_list = batch_list)
        
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

    async def select_callback(self, interaction: disnake.MessageInteraction):

        if interaction.values[0] == "+" or interaction.values[0] == "-":
            self.add_deck_batch_button.disabled = True
            self.add_card_batch_button.disabled = True
        else:
            self.add_deck_batch_button.disabled = False
            self.add_card_batch_button.disabled = False
        super().select_callback(interaction = interaction)
        await interaction.response.edit_message("**Création:** ", view=self)

    async def add_deck_batch_callback(self, interaction: disnake.MessageInteraction):
        """Ajout d'une carte dans la promotion sélectionné

        Parameters
        ---------- 
        """
        batch_id = self.item_dropdown.values[0]
        deck_modal = DeckModal(interaction_id = interaction.id, batch_id = batch_id)
        await interaction.response.send_modal( modal = deck_modal)
        #supression du message initial ou mise à jour de la liste de batch

    async def add_card_batch_callback(self, interaction: disnake.MessageInteraction):
        """Selection d'un élement de la liste pour passer à la suite

        Parameters
        ---------- 
        """
        batch_id = self.item_dropdown.values[0]
        decks_list = self.query.get_decks_list_from_batch(batch_id)
        if(decks_list is not None and len(decks_list) > 0):
            deck_view = DeckSelectView(decks_list)
            await interaction.response.edit_message("Création: ", view = deck_view)
        else:
            await interaction.response.send_message("La Promotion ne contient aucun Deck", ephemeral = True)

    def batch_select_option(self, batch):
        return disnake.SelectOption(
                    label=batch.batch_name,
                    value=str(batch.id)
                )