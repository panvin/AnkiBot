import disnake
from database.query import Query

class CardDropdown(disnake.ui.Select):
    def __init__(self, row, is_disabled, cards_list = None):
        self.update_options(cards_list)

        super().__init__(
            placeholder="Choix de la carte question: ",
            options=self.options,
            row=row,
            disabled=is_disabled
        )

    def update_options(self, cards_list):
        options = []
        if cards_list is not None:
            for card in cards_list:
                card_option = disnake.SelectOption(
                    label = card.card_name,
                    description = f"Deck: {card.deck.deck_name}",
                    value = str(card.id)
                    )
                options.append(card_option)
        self.options=options

class CardView(disnake.ui.View):

    def __init__(self, timeout, cards_list):
        super().__init__(timeout = timeout)
        self.query = Query()
        self.cards_list = cards_list
        
        ########################## Première Ligne

        # Menu déroulant contenant les cartes questions
        self.card_dropdown=CardDropdown(row = 1, is_disabled = False, cards_list=cards_list)
        self.card_dropdown.callback=self.select_card_callback
        self.add_item(self.card_dropdown)

    # Définition des callback des élément graphiques

    def select_card_callback(self, interaction: disnake.MessageInteraction):

        for option in self.card_dropdown.options:
            if option.value == interaction.values[0]:
                option.default = True
            else:
                option.default = False