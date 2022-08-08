import disnake
from ui.anki_embed import AnkiEmbed
from ui.batch_select_view import BatchSelectView
from ui.button_view import AddCardButtonView
from ui.dropdown_view import DropDownView
from ui.modals import DeckModal
from ui.card_management_view import CardManagementView

class DeckManagementView(DropDownView):

    def __init__(self, decks_list):
        placeholder = "Choix du Deck"
        super().__init__(timeout=300.0, fn_select_option = self.deck_select_option, placeholder = placeholder, item_list = decks_list)
        self.decks_list=decks_list
        
        ########################## Seconde Ligne

        # Bouton de création de Deck
        self.add_deck_button=disnake.ui.Button(label = "Ajouter", row = 2, style=disnake.ButtonStyle.green, disabled = False)
        self.add_deck_button.callback=self.add_deck_callback
        self.add_item(self.add_deck_button)
        
        # Bouton d'affichage d'information
        self.show_deck_button=disnake.ui.Button(label = "Infos", row = 2, style=disnake.ButtonStyle.primary, disabled = True)
        self.show_deck_button.callback=self.show_deck_callback
        self.add_item(self.show_deck_button)

        # Bouton d'accès à la gestion des cartes
        self.manage_card_button=disnake.ui.Button(label = "Cartes", row = 2, style=disnake.ButtonStyle.primary, disabled = True)
        self.manage_card_button.callback=self.manage_card_callback
        self.add_item(self.manage_card_button)
        
        # Bouton de mise à jour du nom du deck
        self.update_deck_button=disnake.ui.Button(label = "Modifier", row = 2, style=disnake.ButtonStyle.primary, disabled = True)
        self.update_deck_button.callback=self.update_deck_callback
        self.add_item(self.update_deck_button)

        # Bouton de suppression du deck
        self.delete_deck_button=disnake.ui.Button(label = "Supprimer", row = 2, style=disnake.ButtonStyle.red, disabled = True)
        self.delete_deck_button.callback=self.delete_deck_callback
        self.add_item(self.delete_deck_button)

    # Définition des callback des élément graphiques

    async def select_callback(self, interaction: disnake.MessageInteraction):
        """Foncvtion de mise à jour du menu déroulant 

        Parameters
        ---------- 
        """
        if interaction.values[0] == "+" or interaction.values[0] == "-":
            # Dans le cas où on a choisi un élément de pagination (suivant ou précédent) onb reset l'état des boutons
            self.show_deck_button.disabled   = True
            self.manage_card_button.disabled = True
            self.update_deck_button.disabled = True
            self.delete_deck_button.disabled = True
        else:
            # Au contraire si un deck est sélectionné on active les boutons
            self.show_deck_button.disabled   = False
            self.manage_card_button.disabled = False
            self.update_deck_button.disabled = False
            self.delete_deck_button.disabled = False
        super().select_callback(interaction=interaction)
        await interaction.response.edit_message("**Gestion des Decks:** ", view=self)

    async def add_deck_callback(self, interaction: disnake.MessageInteraction):
        """Création d'un nouveau deck 

        Parameters
        ---------- 
        """
        batches_list = []
        for deck in self.item_list:
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
        """Affichage d'informations et de commandes relatives au Deck affiché 

        Parameters
        ---------- 
        """
        choosen_deck = None
        for deck in self.item_list:
            if deck.id == int(self.item_dropdown.values[0]):
                choosen_deck = deck
                break

        if choosen_deck is not None:
            card_count = self.query.count_cards_in_decks(choosen_deck.id)
            embed = AnkiEmbed().deck_embed(interaction.guild, choosen_deck, card_count)
        await interaction.send(embed = embed, ephemeral=True)
        
    async def manage_card_callback(self, interaction: disnake.MessageInteraction):
        """Accès à l'interface de gestion de Cartes 

        Parameters
        ---------- 
        """
        selected_deck_id=int(self.item_dropdown.values[0])
        card_list = self.query.get_cards_list(selected_deck_id)
        
        if card_list is None or len(card_list) == 0: 
            view = AddCardButtonView(deck_id=selected_deck_id)
            await interaction.response.send_message("Le Deck ne contient aucune Carte question", view = view, ephemeral = True)
        else:
            new_view = CardManagementView(card_list)
            await interaction.response.edit_message("**Gestion des Cartes:** ", view=new_view)
    
    async def update_deck_callback(self, interaction: disnake.MessageInteraction):
        """Mise à jour du nom du Deck 

        Parameters
        ---------- 
        """
        selected_deck_id=int(self.item_dropdown.values[0])
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

    def deck_select_option(self, deck):
        return disnake.SelectOption(
                    label=deck.deck_name,
                    description = f"Promotion: {deck.batch.batch_name}",
                    value=str(deck.id)
        )
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

        