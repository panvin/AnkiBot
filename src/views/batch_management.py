import disnake
from views.dropdown import BatchDropdown
from views.modals import BatchModal
from views.deck_management import DeckManagementView
from database.query import Query

class BatchManagementView(disnake.ui.View):
    message: disnake.Message

    def __init__(self, batch_list):
        super().__init__(timeout=300.0)
        self.query = Query()
        self.batches_list=batch_list
        
        ########################## Première Ligne
        
        # Menu déroulant contenant les decks
        self.batch_dropdown=BatchDropdown(row = 1, is_disabled = False, batch_list = batch_list)
        self.batch_dropdown.callback=self.select_batch_callback
        self.add_item(self.batch_dropdown)

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

    async def select_batch_callback(self, interaction: disnake.MessageInteraction):

        self.show_batch_button.disabled   = False
        self.manage_deck_button.disabled  = False
        self.update_batch_button.disabled = False
        self.delete_batch_button.disabled = False
        for option in self.batch_dropdown.options:
            if option.value == interaction.values[0]:
                option.default = True
            else:
                option.default = False
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
        """Affichage d'informations et de commandes relatives à la promo affichée 

        Parameters
        ---------- 
        """ 
        choosen_batch = None
        for batch in self.batches_list:
            if batch.id == int(self.batch_dropdown.values[0]):
                choosen_batch = batch
                break

        if choosen_batch is not None:
            batch_count = self.query.count_decks_in_batches(choosen_batch.id)
            batch_manager = "Non renseigné"
            batch_manager_id = choosen_batch.batch_manager
            
            # Dans le cas où on a un identifiant de manager
            if batch_manager_id is not None:
                # Dans le cas ou c'est @everyone
                if batch_manager_id == interaction.guild_id:
                    batch_manager = "@everyone" 
                # Dans le cas ou c'est un rôle 
                elif interaction.guild.get_role(batch_manager_id) is not None:
                    batch_manager = f"<@{batch_manager_id}>" 
                # Dans le cas où c'est un utilisateur
                elif interaction.guild.get_role(batch_manager_id) is not None:
                    batch_manager = f"<@!{batch_manager_id}>"
                # Si l'utilisateur est inconnu
                else:
                    batch_manager = f"Utilisateur {batch_manager_id} inconnu"
            message = f"**Promotion:** {choosen_batch.batch_name} - **ID:** {choosen_batch.id}\n**Responsable de la Promotion: **{batch_manager}\n**Nombre de Decks:** {batch_count}"
        else:
            message = "Une erreur s'est produit, impossible d'afficher les informations"
        await interaction.send(message, ephemeral=True)
        #supression du message initial ou mise à jour de la liste de batch
        

    async def manage_deck_callback(self, interaction: disnake.MessageInteraction):
        """Accès à l'interface de gestion de Decks 

        Parameters
        ---------- 
        """
        selected_batch_id=int(self.batch_dropdown.values[0])
        deck_list = self.query.get_decks_list_from_batch(selected_batch_id)
        
        if deck_list is None or len(deck_list) == 0: 
            await interaction.response.send_message("La promotion ne contient aucun Deck", ephemeral = True)
        else:
            new_view = DeckManagementView(deck_list)
            await interaction.response.edit_message("**Gestion des Decks:** ", view=new_view)
    
    async def update_batch_callback(self, interaction: disnake.MessageInteraction):
        """Mise à jour du nom du Batch 

        Parameters
        ---------- 
        """
        selected_batch_id=int(self.batch_dropdown.values[0])
        batch = self.query.get_batch_by_id(selected_batch_id)
        batch_modal = BatchModal(interaction.id, batch)
        await interaction.response.send_modal( modal = batch_modal)
        #supression du message initial ou mise à jour de la liste de batch
        await interaction.send("Mise à jour de la promotion", ephemeral=True)
        
    async def delete_batch_callback(self, interaction: disnake.MessageInteraction):

        await interaction.send("Suppression en cours", ephemeral=True)
        # await interaction.delete_original_message(10)

    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

        