import disnake
from views.dropdown import Dropdown

class DropdownView(disnake.ui.View):
    def __init__(self):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(Dropdown(["Un", "Deux", "Trois"]))
        self.add_item(Dropdown(["Quatre", "Cinq", "Six"]))
        self.add_item(Dropdown(["Sept", "Huit", "Neuf"]))