import disnake

class DeckDropdown(disnake.ui.Select):
    def __init__(self, row, is_disabled, deck_list):
        options = []
        for deck in deck_list:
            deck_option = disnake.SelectOption(
                label=deck.deck_name,
                value=deck.id
            )
            options.append(deck_option)

        super().__init__(
            custom_id="deck_dropdown",
            placeholder="Choix du deck",
            min_values=1,
            max_values=1,
            options=options,
            row=row,
            disabled=is_disabled,
        )

class CardDropdown(disnake.ui.Select):
    def __init__(self, row, is_disabled, card_list):
        options = []
        for card in card_list:
            card_option = disnake.SelectOption(
                label=card.card_name,
                value=card.id
            )
            options.append(card_option)

        super().__init__(
            placeholder="Choix de la carte question: ",
            min_values=1,
            max_values=1,
            options=options,
            row=row,
            disabled=is_disabled
        )