import disnake
from ui.deck_download_view import DeckDownloadView
from ui.deck_select_view import DeckSelectView
from ui.dropdown_view import DropDownView
from ui.modals import  DeckModal

class BatchDownloadView(DropDownView):

    def __init__(self, batch_list):
        placeholder = "Choix de la Promotion"
        super().__init__(timeout=300.0, fn_select_option = self.batch_select_option, placeholder = placeholder, item_list = batch_list)
        
        ########################## Seconde Ligne
        
        # Bouton pour télécharger l'ensemble des decks d'une promotion
        self.download_batch_button=disnake.ui.Button(label = "Télécharger tous les Decks", emoji = "📦", row = 2, style=disnake.ButtonStyle.green, disabled = True)
        self.download_batch_button.callback=self.download_batch_callback
        self.add_item(self.download_batch_button)

        # Bouton pour aller à la page de téléchargement d'un deck
        self.download_deck_button=disnake.ui.Button(label = "Télécharger un Deck", emoji = "📩", row = 2, style=disnake.ButtonStyle.green, disabled = True)
        self.download_deck_button.callback=self.dowload_deck_callback
        self.add_item(self.download_deck_button)
        
    # Définition des callback des élément graphiques

    async def select_callback(self, interaction: disnake.MessageInteraction):

        if interaction.values[0] == "+" or interaction.values[0] == "-":
            self.download_batch_button.disabled = True
            self.download_deck_button.disabled = True
        else:
            self.download_batch_button.disabled = False
            self.download_deck_button.disabled = False
        super().select_callback(interaction = interaction)
        await interaction.response.edit_message("**Création:** ", view=self)

    async def download_batch_callback(self, interaction: disnake.MessageInteraction):
        """Ajout d'une carte dans la promotion sélectionné

        Parameters
        ---------- 
        """
        batch_id = self.item_dropdown.values[0]
        await interaction.response.send_message(f"On va télécharger tous les decks de {batch_id}",  ephemeral = True)

    async def dowload_deck_callback(self, interaction: disnake.MessageInteraction):
        """Selection d'un élement de la liste pour passer à la suite

        Parameters
        ---------- 
        """
        batch_id = self.item_dropdown.values[0]
        decks_list = self.query.get_decks_list_from_batch(batch_id)
        if(decks_list is not None and len(decks_list) > 0):
            deck_view = DeckDownloadView(decks_list)
            await interaction.response.edit_message("Création: ", view = deck_view)
        else:
            await interaction.response.send_message("La Promotion ne contient aucun Deck", ephemeral = True)

    async def get_zipped_batch(self, batch_id):
        self.query.get_decks_list_from_batch()

    def batch_select_option(self, batch):
        return disnake.SelectOption(
                    label=batch.batch_name,
                    value=str(batch.id)
                )