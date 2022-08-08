import disnake
from database.query import Query

class DeckDropdown(disnake.ui.Select):
    def __init__(self, row, is_disabled, deck_list=None):
        self.update_options(deck_list)

        super().__init__(
            custom_id="deck_dropdown",
            placeholder="Choix du deck",
            options=self.options,
            row=row,
            disabled=is_disabled,
        )
    
    def update_options(self, deck_list):
        options = []
        if deck_list is not None:
            for deck in deck_list:
                deck_option = disnake.SelectOption(
                    label=deck.deck_name,
                    description = f"Promotion: {deck.batch.batch_name}",
                    value=str(deck.id)
                )
                options.append(deck_option)
        self.options=options

class DeckView(disnake.ui.View):

    def __init__(self, timeout, decks_list):
        super().__init__(timeout = timeout)
        self.query = Query()
        self.decks_list=decks_list
        
        ########################## Première Ligne
        
        # Menu déroulant contenant les decks
        self.deck_dropdown=DeckDropdown(row = 1, is_disabled = False, deck_list = decks_list)
        self.deck_dropdown.callback=self.select_deck_callback
        self.add_item(self.deck_dropdown)

    # Définition des callback des élément graphiques

    def select_deck_callback(self, interaction: disnake.MessageInteraction):
                
        for option in self.deck_dropdown.options:
            if option.value == interaction.values[0]:
                option.default = True
            else:
                option.default = False
                interaction.message