import disnake
from ui.anki_embed import AnkiEmbed
from ui.dropdown_view import DropDownView
from ui.modals import BatchModal
from ui.deck_management_view import DeckManagementView
from ui.button_view import AddDeckButtonView

class BatchManagementView(DropDownView):

    def __init__(self, batch_list):
        placeholder = "Choix de la Promotion"
        super().__init__(timeout=300.0, fn_select_option = self.batch_select_option, placeholder = placeholder, item_list = batch_list)
        
        ########################## Seconde Ligne
        
        # Bouton d'ajout de promotions
        self.add_batch_button=disnake.ui.Button(label = "Ajouter", row = 2, style=disnake.ButtonStyle.green, disabled = False)
        self.add_batch_button.callback=self.add_batch_callback
        self.add_item(self.add_batch_button)
        
        # Bouton d'affichage d'information
        self.show_batch_button=disnake.ui.Button(label = "Infos", row = 2, style=disnake.ButtonStyle.primary, disabled = True)
        self.show_batch_button.callback=self.show_batch_callback
        self.add_item(self.show_batch_button)

        # Bouton permettant l'accès à la gestion de deck
        self.manage_deck_button=disnake.ui.Button(label = "Decks", row = 2, style=disnake.ButtonStyle.primary, disabled = True)
        self.manage_deck_button.callback=self.manage_deck_callback
        self.add_item(self.manage_deck_button)
        
        # Bouton de mise à jour de la promotion
        self.update_batch_button=disnake.ui.Button(label = "Modifier", row = 2, style=disnake.ButtonStyle.primary, disabled = True)
        self.update_batch_button.callback=self.update_batch_callback
        self.add_item(self.update_batch_button)

        # Bouton de suppression
        self.delete_batch_button=disnake.ui.Button(label = "Supprimer", row = 2, style=disnake.ButtonStyle.red, disabled = True)
        self.delete_batch_button.callback=self.delete_batch_callback
        self.add_item(self.delete_batch_button)

    # Définition des callback des élément graphiques

    async def select_callback(self, interaction: disnake.MessageInteraction):

        if interaction.values[0] == "+" or interaction.values[0] == "-":
            self.show_batch_button.disabled   = True
            self.manage_deck_button.disabled  = True
            self.update_batch_button.disabled = True
            self.delete_batch_button.disabled = True
        else:
            self.show_batch_button.disabled   = False
            self.manage_deck_button.disabled  = False
            self.update_batch_button.disabled = False
            self.delete_batch_button.disabled = False
        super().select_callback(interaction = interaction)
        await interaction.response.edit_message("**Gestion des Promotions:** ", view=self)

    async def add_batch_callback(self, interaction: disnake.MessageInteraction):
        """Création d'une nouvelle promotion 

        Parameters
        ---------- 
        """
        batch_modal = BatchModal(interaction.id)
        await interaction.response.send_modal( modal = batch_modal)
        #supression du message initial ou mise à jour de la liste de batch

    async def show_batch_callback(self, interaction: disnake.MessageInteraction):
        """Affichage d'informations et de commandes relatives à la Promotion affichée 

        Parameters
        ---------- 
        """ 
        choosen_batch = None
        for batch in self.item_list:
            if batch.id == int(self.item_dropdown.values[0]):
                choosen_batch = batch
                break

        if choosen_batch is not None:
            batch_count = self.query.count_decks_in_batches(choosen_batch.id)
            embed = AnkiEmbed().batch_embed(interaction.guild, choosen_batch, batch_count)
        await interaction.send(embed = embed, ephemeral=True)        

    async def manage_deck_callback(self, interaction: disnake.MessageInteraction):
        """Accès à l'interface de gestion de Decks 

        Parameters
        ---------- 
        """
        selected_batch_id=int(self.item_dropdown.values[0])
        deck_list = self.query.get_decks_list_from_batch(selected_batch_id)
        
        if deck_list is None or len(deck_list) == 0: 
            view = AddDeckButtonView(selected_batch_id)
            await interaction.response.send_message("La Promotion ne contient aucun Deck", view = view, ephemeral = True)
        else:
            new_view = DeckManagementView(deck_list)
            await interaction.response.edit_message("**Gestion des Decks:** ", view=new_view)
    
    async def update_batch_callback(self, interaction: disnake.MessageInteraction):
        """Mise à jour du nom du Batch 

        Parameters
        ---------- 
        """
        selected_batch_id=int(self.item_dropdown.values[0])
        batch = self.query.get_batch_by_id(selected_batch_id)
        batch_modal = BatchModal(interaction.id, batch)
        await interaction.response.send_modal( modal = batch_modal)
        #supression du message initial ou mise à jour de la liste de batch
        await interaction.send("Mise à jour de la promotion", ephemeral=True)
        
    async def delete_batch_callback(self, interaction: disnake.MessageInteraction):

        await interaction.send("Suppression en cours", ephemeral=True)

    def batch_select_option(self, batch):
        return disnake.SelectOption(
                    label=batch.batch_name,
                    value=str(batch.id)
                )