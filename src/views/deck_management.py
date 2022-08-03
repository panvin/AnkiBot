import disnake
from views.dropdown import DeckDropdown

class DeckManagementView(disnake.ui.View):

    def __init__(self, decks_list):
        super().__init__(timeout=30.0)
        self.decks_list=decks_list
        self.deck_options = []
        self.card_list = None
        self.card_options = []
        
        ########################## Première Ligne
        
        # Menu déroulant contenant les decks
        self.deck_dropdown=DeckDropdown(row = 1, is_disabled = False, deck_list = decks_list)
        self.deck_dropdown.callback=self.select_deck_callback
        self.add_item(self.deck_dropdown)

        ########################## Seconde Ligne

        # Bouton d'affichage d'information
        self.show_deck_button=disnake.ui.Button(label = "Ajouter une carte", row = 2, style=disnake.ButtonStyle.primary, disabled = True)
        self.show_deck_button.callback=self.afficher_deck_callback
        self.add_item(self.show_deck_button)
        
        # Bouton d'affichage de modification
        self.update_deck_button=disnake.ui.Button(label = "Modifier", row = 2, style=disnake.ButtonStyle.green, disabled = True)
        self.update_deck_button.callback=self.update_deck_callback
        self.add_item(self.update_deck_button)

        # Bouton de suppression
        self.delete_deck_button=disnake.ui.Button(label = "Supprimer", row = 2, style=disnake.ButtonStyle.red, disabled = True)
        self.delete_deck_button.callback=self.delete_deck_callback
        self.add_item(self.delete_deck_button)

    # Définition des callback des élément graphiques

    async def select_deck_callback(self, interaction: disnake.MessageInteraction):

        self.show_deck_button.disabled = False
        self.update_deck_button.disabled = False
        self.delete_deck_button.disabled = False
        for option in self.deck_dropdown.options:
            if option.value == interaction.values[0]:
                option.default = True
            else:
                option.default = False
        await interaction.response.edit_message("**Gestion des decks:** ", view=self)

    async def afficher_deck_callback(self, interaction: disnake.MessageInteraction):

        self.update_deck_button.disabled = False
        self.delete_deck_button.disabled = False
        await interaction.send(f"Modification en cours {self.deck_dropdown.values}", ephemeral=True)
    
    
    async def update_deck_callback(self, interaction: disnake.MessageInteraction):

        
        self.update_deck_button.disabled = False
        self.delete_deck_button.disabled = False
        await interaction.send("Modification en cours", ephemeral=True)
        
    async def delete_deck_callback(self, interaction: disnake.MessageInteraction):

        await interaction.send("Suppression en cours", ephemeral=True)

    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

        