import disnake
from database.query import Query

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

class BatchView(disnake.ui.View):

    def __init__(self, timeout, batch_list):
        super().__init__(timeout = timeout)
        self.query = Query()
        self.batches_list=batch_list
        
        ########################## Première Ligne
        
        # Menu déroulant contenant les decks
        self.batch_dropdown=BatchDropdown(row = 1, is_disabled = False, batch_list = batch_list)
        self.batch_dropdown.callback=self.select_batch_callback
        self.add_item(self.batch_dropdown)

    # Définition des callback des élément graphiques

    def select_batch_callback(self, interaction: disnake.MessageInteraction):

        for option in self.batch_dropdown.options:
            if option.value == interaction.values[0]:
                option.default = True
            else:
                option.default = False