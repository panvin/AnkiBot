import disnake
from ui.batch_select_view import BatchSelectView
from ui.deck_view import DeckView
from database.query import Query
from ui.modals import DeckModal
from ui.card_management_view import CardManagementView

class DeckManagementView(DeckView):

    def __init__(self, decks_list):
        super().__init__(timeout=300.0, decks_list = decks_list)
        self.decks_list=decks_list
        
        ########################## Seconde Ligne

        # Bouton d'affichage d'information
        self.add_deck_button=disnake.ui.Button(label = "Ajouter", row = 2, style=disnake.ButtonStyle.green, disabled = False)
        self.add_deck_button.callback=self.add_deck_callback
        self.add_item(self.add_deck_button)
        
        # Bouton d'affichage d'information
        self.show_deck_button=disnake.ui.Button(label = "Infos", row = 2, style=disnake.ButtonStyle.primary, disabled = True)
        self.show_deck_button.callback=self.show_deck_callback
        self.add_item(self.show_deck_button)

        # Bouton d'affichage d'information
        self.manage_card_button=disnake.ui.Button(label = "Cartes", row = 2, style=disnake.ButtonStyle.primary, disabled = True)
        self.manage_card_button.callback=self.manage_card_callback
        self.add_item(self.manage_card_button)
        
        # Bouton d'affichage de modification
        self.update_deck_button=disnake.ui.Button(label = "Modifier", row = 2, style=disnake.ButtonStyle.primary, disabled = True)
        self.update_deck_button.callback=self.update_deck_callback
        self.add_item(self.update_deck_button)

        # Bouton de suppression
        self.delete_deck_button=disnake.ui.Button(label = "Supprimer", row = 2, style=disnake.ButtonStyle.red, disabled = True)
        self.delete_deck_button.callback=self.delete_deck_callback
        self.add_item(self.delete_deck_button)

    # Définition des callback des élément graphiques

    async def select_deck_callback(self, interaction: disnake.MessageInteraction):
        self.show_deck_button.disabled   = False
        self.manage_card_button.disabled = False
        self.update_deck_button.disabled = False
        self.delete_deck_button.disabled = False
        super().select_deck_callback(interaction=interaction)
        await interaction.response.edit_message("**Gestion des decks:** ", view=self)

    async def add_deck_callback(self, interaction: disnake.MessageInteraction):
        """Création d'un nouveau deck 

        Parameters
        ---------- 
        """
        batches_list = []
        for deck in self.decks_list:
            if deck.batch_id is not None and deck.batch_id not in batches_list:
                batches_list.append(deck.batch_id)

        if batches_list is None or len(batches_list) == 0:
            await interaction.response.send_message(" Vous n'êtes membre d'aucune promotion", ephemeral=True)
        elif len(batches_list) == 1:
            deck_modal = DeckModal(interaction_id = interaction.id, batch_id = batches_list[0])
            await interaction.response.send_modal( modal = deck_modal)
        else:
            deck_view = BatchSelectView(batches_list)
            await interaction.response.edit_message( "Création:" , view = deck_view, ephemeral = True)

    async def show_deck_callback(self, interaction: disnake.MessageInteraction):
        
        choosen_deck = None
        for deck in self.decks_list:
            if deck.id == int(self.deck_dropdown.values[0]):
                choosen_deck = deck
                break

        if choosen_deck is not None:
            card_count = self.query.count_cards_in_decks(choosen_deck.id)
            deck_manager = "Non renseigné"
            deck_manager_id = choosen_deck.deck_manager
            # Dans le cas où on a un identifiant de manager
            if deck_manager_id is not None:
                # Dans le cas ou c'est @everyone
                if deck_manager_id == interaction.guild_id:
                    batch_manager = "@everyone" 
                # Dans le cas ou c'est un rôle 
                elif interaction.guild.get_role(deck_manager_id) is not None:
                    batch_manager = f"<@{deck_manager_id}>" 
                # Dans le cas où c'est un utilisateur
                elif interaction.guild.get_member(deck_manager_id) is not None:
                    batch_manager = f"<@!{deck_manager_id}>"
                # Si l'utilisateur est inconnu
                else:
                    batch_manager = f"Utilisateur {deck_manager_id} inconnu"
            message = f"**Deck:** {choosen_deck.deck_name} - **ID:** {choosen_deck.id}\n**Responsable du deck: **{deck_manager}\n**Nombre de Cartes:** {card_count}"
        else:
            message = "Une erreur s'est produit, impossible d'afficher les informations"
        await interaction.send(message, ephemeral=True)

    async def manage_card_callback(self, interaction: disnake.MessageInteraction):
        selected_deck_id=int(self.deck_dropdown.values[0])
        card_list = self.query.get_cards_list(selected_deck_id)
        
        if card_list is None or len(card_list) == 0: 
            await interaction.response.send_message("Le Deck ne contient aucune carte", ephemeral = True)
        else:
            new_view = CardManagementView(card_list)
            await interaction.response.edit_message("**Gestion des Cartes:** ", view=new_view)
    
    async def update_deck_callback(self, interaction: disnake.MessageInteraction):
        """Mise à jour du nom du Deck 

        Parameters
        ---------- 
        """
        selected_deck_id=int(self.deck_dropdown.values[0])
        deck = self.query.get_deck_by_id(selected_deck_id)
        deck_modal = DeckModal(interaction_id = interaction.id, batch_id = deck.batch_id, deck = deck)
        await interaction.response.send_modal( modal = deck_modal)
        #supression du message initial ou mise à jour de la liste de batch
        

        await interaction.send("Modification en cours", ephemeral=True)
        
    async def delete_deck_callback(self, interaction: disnake.MessageInteraction):

        await interaction.send("Suppression en cours", ephemeral=True)

    
    def get_available_batches(self, member : disnake.Member):
        #On récupère les identifiants de roles
        role_id = []
        for role in member.roles:
            role_id.append(role.id)
        return self.query.get_batches_from_roles(role_list = role_id)

    def get_available_decks(self, member : disnake.Member):
        role_id = []
        for role in member.roles:
            role_id.append(role.id)
        return self.query.get_decks_from_roles(role_list = role_id)

    def get_available_cards(self, member : disnake.Member):
        role_id = []
        for role in member.roles:
            role_id.append(role.id)
        return self.query.get_cards_from_roles(role_list = role_id)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

        