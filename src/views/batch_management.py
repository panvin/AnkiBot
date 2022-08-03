import disnake
from views.dropdown import BatchDropdown

class BatchManagementView(disnake.ui.View):
    message: disnake.Message

    def __init__(self, batch_list):
        super().__init__(timeout=30.0)
        self.batches_list=batch_list
        
        ########################## Première Ligne
        
        # Menu déroulant contenant les decks
        self.batch_dropdown=BatchDropdown(row = 1, is_disabled = False, batch_list = batch_list)
        self.batch_dropdown.callback=self.select_batch_callback
        self.add_item(self.batch_dropdown)

        ########################## Seconde Ligne

        # Bouton d'affichage d'information
        self.add_batch_button=disnake.ui.Button(label = "Ajouter une promo", row = 2, style=disnake.ButtonStyle.primary, disabled = False)
        self.add_batch_button.callback=self.add_batch_callback
        self.add_item(self.add_batch_button)

        # Bouton d'affichage d'information
        self.manage_deck_button=disnake.ui.Button(label = "Gestion de deck", row = 2, style=disnake.ButtonStyle.secondary, disabled = True)
        self.manage_deck_button.callback=self.manage_deck_callback
        self.add_item(self.manage_deck_button)
        
        # Bouton d'affichage de modification
        self.update_batch_button=disnake.ui.Button(label = "Modifier", row = 2, style=disnake.ButtonStyle.green, disabled = True)
        self.update_batch_button.callback=self.update_batch_callback
        self.add_item(self.update_batch_button)

        # Bouton de suppression
        self.delete_batch_button=disnake.ui.Button(label = "Supprimer", row = 2, style=disnake.ButtonStyle.red, disabled = True)
        self.delete_batch_button.callback=self.delete_batch_callback
        self.add_item(self.delete_batch_button)

    # Définition des callback des élément graphiques

    async def select_batch_callback(self, interaction: disnake.MessageInteraction):

        self.manage_deck_button.disabled = False
        self.update_batch_button.disabled = False
        self.delete_batch_button.disabled = False
        for option in self.batch_dropdown.options:
            if option.value == interaction.values[0]:
                option.default = True
            else:
                option.default = False
        await interaction.response.edit_message("**Gestion des Promotions:** ", view=self)

    async def add_batch_callback(self, interaction: disnake.MessageInteraction):

        await interaction.send("Ajout d'une promotion", ephemeral=True)

    async def manage_deck_callback(self, interaction: disnake.MessageInteraction):
        selected_batch_id=int(self.batch_dropdown.values[0])
        bot = interaction.bot
        await interaction.send("Gestion des decks", ephemeral=True)
        #await bot.invoke(bot.get_command("manage_decks"), batch_id = selected_batch_id)
        #await interaction.bot.get_slash_command("manage_decks").callback(inter =interaction, batch_id = selected_batch_id)    
    
    async def update_batch_callback(self, interaction: disnake.MessageInteraction):

        await interaction.send("Mise à jour de la promotion", ephemeral=True)
        
    async def delete_batch_callback(self, interaction: disnake.MessageInteraction):

        await interaction.send("Suppression en cours", ephemeral=True)
        # await interaction.delete_original_message(10)

    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

        