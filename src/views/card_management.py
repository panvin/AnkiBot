import disnake
from views.dropdown import CardDropdown

class CardManagementView(disnake.ui.View):
    message: disnake.Message

    def __init__(self, deck_id, card_list):
        super().__init__(timeout=30.0)
        self.card_list=card_list
        self.deck_id=deck_id
        
        ########################## Première Ligne

        # Menu déroulant contenant les cartes questions
        self.card_dropdown=CardDropdown(row = 1, is_disabled = False, card_list=card_list)
        self.card_dropdown.callback=self.select_card_callback
        self.add_item(self.card_dropdown)

        ########################## Seconde Ligne

        # Bouton d'affichage d'information
        self.update_card_button=disnake.ui.Button(label = "Afficher", row = 2, style=disnake.ButtonStyle.primary, disabled = True)
        self.update_card_button.callback=self.show_card_callback
        self.add_item(self.update_card_button)
        
        # Bouton d'affichage de modification
        self.update_card_button=disnake.ui.Button(label = "Modifier", row = 2, style=disnake.ButtonStyle.green, disabled = True)
        self.update_card_button.callback=self.update_card_callback
        self.add_item(self.update_card_button)

        # Bouton de suppression
        self.delete_card_button=disnake.ui.Button(label = "Supprimer", row = 2, style=disnake.ButtonStyle.red, disabled = True)
        self.delete_card_button.callback=self.delete_card_callback
        self.add_item(self.delete_card_button)

    # Définition des callback des élément graphiques

    async def select_card_callback(self, interaction: disnake.MessageInteraction):

        self.update_card_button.disabled = False
        self.delete_card_button.disabled = False
        for option in self.card_dropdown.options:
            if option.value == interaction.values[0]:
                option.default = True
            else:
                option.default = False
        await interaction.response.edit_message("**Gestion des Cartes:** ", view=self)

    async def show_card_callback(self, interaction: disnake.MessageInteraction):

        self.update_card_button.disabled = False
        self.delete_card_button.disabled = False
        await interaction.response.edit_message("**Gestion des decks:** ", view=self)
    
    
    async def update_card_callback(self, interaction: disnake.MessageInteraction):

        await interaction.send("Modification en cours", ephemeral=True)
        await interaction.delete_original_message(10)

    async def delete_card_callback(self, interaction: disnake.MessageInteraction):

        await interaction.send("Suppression en cours", ephemeral=True)
        await interaction.delete_original_message(10)


    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

        