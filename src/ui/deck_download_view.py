import disnake
from database.query import Query
from ui.dropdown_view import DropDownView
from ui.modals import CardModal

class DeckDownloadView(DropDownView):

    def __init__(self, decks_list):
        placeholder = "Choix du Deck à télécharger"
        super().__init__(timeout=300.0, fn_select_option = self.deck_select_option, placeholder = placeholder, item_list = decks_list)

        
        ########################## Seconde Ligne

        
        # Bouton de Téléchargement de Decks
        self.download_deck_button=disnake.ui.Button(label = "Télécharger", emoji = "📩", row = 2, style=disnake.ButtonStyle.green, disabled = True)
        self.download_deck_button.callback=self.download_deck_callback
        self.add_item(self.download_deck_button)

    # Définition des callback des élément graphiques

    async def select_callback(self, interaction: disnake.MessageInteraction):
        if interaction.values[0] == "+" or interaction.values[0] == "-":
            self.download_deck_button.disabled   = True
        else:
            self.download_deck_button.disabled   = False
        super().select_callback(interaction = interaction)
        await interaction.response.edit_message("**Téléchargement:**", view=self)

    async def download_deck_callback(self, interaction: disnake.MessageInteraction):
        """Téléchargement de decks 

        Parameters
        ---------- 
        """
        selected_deck_id = self.item_dropdown.values
        selected_deck = None
        for deck in self.item_list:
            if selected_deck_id == deck.id:
                selected_deck = deck
                break

        if deck is not None and deck.is_updated:
            # On crée le fichier Anki
            print("on essaie ubn truc")
        elif deck is not None:
            # On envoie directement le fichier
            print("on essaie ubn truc")
        else:
            await interaction.response.send_message( "Une erreur s'est produite", ephemeral = True)
        
        await self.download_anki_file(deck)
        await interaction.response.send_message( "Téléchargement en cours!!!", ephemeral = True)

    async def download_anki_file(self, deck):
        """Téléchargement de decks 

        Parameters
        ---------- 
        """
        selected_decks = self.item_dropdown.values
        print(selected_decks)
        await interaction.response.send_message( "Téléchargement en cours!!!", ephemeral = True)

    def deck_select_option(self, deck):
        return disnake.SelectOption(
                    label=deck.deck_name,
                    description = f"Promotion: {deck.batch.batch_name}",
                    value=str(deck.id)
        )