import disnake
from database.query import Query
from ui.dropdown_view import DropDownView
from ui.modals import CardModal

class DeckSelectView(DropDownView):

    def __init__(self, decks_list):
        placeholder = "Choix du Deck"
        super().__init__(timeout=300.0, fn_select_option = self.deck_select_option, placeholder = placeholder, item_list = decks_list)

        ########################## Seconde Ligne

        # Bouton d'affichage d'information
        self.add_card_button=disnake.ui.Button(label = "Ajouter", row = 2, style=disnake.ButtonStyle.green, disabled = True)
        self.add_card_button.callback=self.add_card_callback
        self.add_item(self.add_card_button)

    # Définition des callback des élément graphiques

    async def select_callback(self, interaction: disnake.MessageInteraction):
        if interaction.values[0] == "+" or interaction.values[0] == "-":
            self.add_card_button.disabled   = True
        else:
            self.add_card_button.disabled   = False
        super().select_callback(interaction = interaction)
        await interaction.response.edit_message("**Création:** ", view=self)

    async def add_card_callback(self, interaction: disnake.MessageInteraction):
        """Création d'une nouvelle carte 

        Parameters
        ---------- 
        """
        selected_deck = self.item_dropdown.values[0]
        card_modal = CardModal(interaction_id=interaction.id, deck_id = selected_deck) 
        await interaction.response.send_modal( modal = card_modal)

    def deck_select_option(self, deck):
        return disnake.SelectOption(
                    label=deck.deck_name,
                    description = f"Promotion: {deck.batch.batch_name}",
                    value=str(deck.id)
        )