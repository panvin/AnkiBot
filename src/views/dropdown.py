import disnake

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

class CardDropdown(disnake.ui.Select):
    def __init__(self, row, is_disabled, card_list = None):
        self.update_options(card_list)

        super().__init__(
            placeholder="Choix de la carte question: ",
            options=self.options,
            row=row,
            disabled=is_disabled
        )

    def update_options(self, card_list):
        options = []
        if card_list is not None:
            for card in card_list:
                card_option = disnake.SelectOption(
                    label = card.card_name,
                    description = f"Deck: {card.deck.deck_name}",
                    value = str(card.id)
                    )
                options.append(card_option)
        self.options=options

class BatchDropdown(disnake.ui.Select):
    def __init__(self, row, is_disabled, batch_list=None):
        self.update_options(batch_list)

        super().__init__(
            placeholder="Choix de la promo: ",
            options=self.options,
            row=row,
            disabled=is_disabled
        )

    def update_options(self, batch_list):
        options = []
        if batch_list is not None:
            for batch in batch_list:
                batch_option = disnake.SelectOption(
                    label=batch.batch_name,
                    value=str(batch.id)
                )
                options.append(batch_option)
        self.options=options