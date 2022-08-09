import disnake
from database.query import Query

class Dropdown(disnake.ui.Select):
    def __init__(self, row, is_disabled, fn_select_option, placeholder, item_list=None):
        
        self.select_options_list = []
        self.generate_options(item_list, fn_select_option)
        previous =[disnake.SelectOption(
                        label = "Précédent",
                        emoji="⏮️",
                        value = "+"
                        )]
        next = [disnake.SelectOption(
                        label = "Suivant",
                        emoji="⏭️",
                        value = "-"
                        )]

        self.indexed_option = []
        self.index = 0

        if(len(self.select_options_list) > 25):
            chunk = self.select_options_list[0:24] + next
            self.indexed_option.append(chunk)
            i = 24
            while len(self.select_options_list) - i > 23:
                chunk = previous + self.select_options_list[i:i+23] + next
                self.indexed_option.append(chunk)
                i = i+23
            chunk = previous + self.select_options_list[i:]
            self.indexed_option.append(chunk)
        else:
            self.indexed_option.append(self.select_options_list)

        super().__init__(
            placeholder=placeholder,
            options=self.indexed_option[self.index],
            row=row,
            disabled=is_disabled,
        )
    
    def generate_options(self, item_list, fn_select_option):
        if item_list is not None:
            for item in item_list:
                deck_option = fn_select_option(item)
                self.select_options_list.append(deck_option)

    def update_options(self, value : str):
        if value == "+":
            self.index += 1
        elif value == "-":
            self.index -= 1
        self.options = self.indexed_option[self.index]

class DropDownView(disnake.ui.View):

    def __init__(self, timeout, fn_select_option, placeholder, item_list):
        super().__init__(timeout = timeout)
        self.query = Query()
        self.item_list=item_list
        
        ########################## Première Ligne
        
        # Menu déroulant contenant les decks
        self.item_dropdown=Dropdown(row = 1, is_disabled = False, fn_select_option = fn_select_option, placeholder = placeholder ,item_list = item_list)
        self.item_dropdown.callback=self.select_callback
        self.add_item(self.item_dropdown)

    # Définition des callback des élément graphiques

    def select_callback(self, interaction: disnake.MessageInteraction):

        if "+" in interaction.values or "-" in interaction.values:

            for option in self.item_dropdown.options:
                option.default = False
            if "+" in interaction.values:
                interaction.values.remove("+")
                self.item_dropdown.update_options(value = "+")
            elif "-" in interaction.values:
                interaction.values.remove("-")
                self.item_dropdown.update_options(value = "-")
            
        else:   
            for option in self.item_dropdown.options:
                if option.value in interaction.values:
                    option.default = True
                else:
                    option.default = False