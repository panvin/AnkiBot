from disnake.ext import commands
from  disnake.utils import get
from database.query import Query
from views.batch_management import BatchManagementView
from views.deck_management  import DeckManagementView
from views.card_management import CardManagementView
from disnake import Colour, Embed
import disnake
import asyncio
import re


class SlashCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.query = Query()
    
    
###########################################################################################################################

    @commands.slash_command()
    async def send_ephemeral(self, inter: disnake.CommandInteraction):
        """On envoie un petit message éphémère

        Parameters
        ----------
        category: The category to search
        item: The item to display
        details: Whether to get the details of this time
        """
        # Sends a modal using a high level implementation.
        await inter.response.send_message("Ceci est un message éphémère", ephemeral=True)

    @commands.slash_command(description="Affiche la liste des decks")
    async def show_deck_list(self, inter: disnake.CommandInteraction):
        # Sends a modal using a high level implementation.
        
        deck_list= self.query.get_decks_list(inter.guild_id)

        deck_list_as_string = ''

        for deck in deck_list:
            deck_list_as_string = deck_list_as_string.join(f"{deck.id} : {deck.deck_name}\n")

        embed = Embed(title="Liste des commandes disponibles: ", color=Colour.gold())
        embed.add_field(name="id : Nom du module", value=deck_list_as_string, inline=False)

        await inter.response.send_message(embed=embed, ephemeral=True)

    

###########################################################################################################################

    # Create a Deck with Modal
    @commands.slash_command(description = "Création d'un nouveau deck")
    async def create_batch(self, inter: disnake.CommandInteraction):
        """Création d'un nouveau deck 

        Parameters
        ---------- 
        """
        await inter.response.send_modal(
            title="Créer un Deck",
            custom_id="create_deck_custom_id",
            components=[
                disnake.ui.TextInput(
                    label="Nom",
                    placeholder="Le nom du deck à créer",
                    custom_id="name",
                    style=disnake.TextInputStyle.short,
                    min_length=3,
                    max_length=100
                )
            ],
        )

        # Waits until the user submits the modal.
        try:
            modal_inter: disnake.ModalInteraction = await self.bot.wait_for(
                "modal_submit",
                check=lambda i: i.custom_id == "create_deck_custom_id" and i.author.id == inter.author.id,
                timeout=300,
            )
        except asyncio.TimeoutError:
            # The user didn't submit the modal in the specified period of time.
            # This is done since Discord doesn't dispatch any event for when a modal is closed/dismissed.
            return

        deck_name = modal_inter.text_values.get("name").capitalize()
        
        deck=self.query.create_deck(server_id = inter.guild_id, deck_name = deck_name)

        embed = self.confirmation_deck_embed(deck_name = deck_name, deck_id = deck.id)
        await modal_inter.response.send_message(embed=embed, ephemeral=True)
    
    
    # Create a Deck with Modal
    @commands.slash_command(description = "Création d'un nouveau deck")
    async def create_deck(self, inter: disnake.CommandInteraction):
        """Création d'un nouveau deck 

        Parameters
        ---------- 
        """
        await inter.response.send_modal(
            title="Créer un Deck",
            custom_id="create_deck_custom_id",
            components=[
                disnake.ui.TextInput(
                    label="Nom",
                    placeholder="Le nom du deck à créer",
                    custom_id="name",
                    style=disnake.TextInputStyle.short,
                    min_length=3,
                    max_length=100
                )
            ],
        )

        # Waits until the user submits the modal.
        try:
            modal_inter: disnake.ModalInteraction = await self.bot.wait_for(
                "modal_submit",
                check=lambda i: i.custom_id == "create_deck_custom_id" and i.author.id == inter.author.id,
                timeout=300,
            )
        except asyncio.TimeoutError:
            # The user didn't submit the modal in the specified period of time.
            # This is done since Discord doesn't dispatch any event for when a modal is closed/dismissed.
            return

        deck_name = modal_inter.text_values.get("name").capitalize()
        
        deck=self.query.create_deck(server_id = inter.guild_id, deck_name = deck_name)

        embed = self.confirmation_deck_embed(deck_name = deck_name, deck_id = deck.id)
        await modal_inter.response.send_message(embed=embed, ephemeral=True)

    @commands.slash_command()
    async def create_card(self, inter: disnake.CommandInteraction):
        # Works same as the above code but using a low level interface.
        # It's recommended to use this if you don't want to increase cache usage.
        await inter.response.send_modal(
            title="Ajout de carte à un deck",
            custom_id="create_card",
            components = [
                disnake.ui.TextInput(
                    label="Question",
                    placeholder="Question à ajouter au deck",
                    custom_id="question",
                    style=disnake.TextInputStyle.short,
                    min_length=3,
                    max_length=500,
                ),
                disnake.ui.TextInput(
                    label="Réponse",
                    placeholder="Réponse",
                    custom_id="reponse",
                    style=disnake.TextInputStyle.paragraph,
                    min_length=3,
                    max_length=4000,
                ),
            ],
        )

        # Waits until the user submits the modal.
        try:
            modal_inter: disnake.ModalInteraction = await self.bot.wait_for(
                "modal_submit",
                check=lambda i: i.custom_id == "create_card" and i.author.id == inter.author.id,
                timeout=300,
            )
        except asyncio.TimeoutError:
            # The user didn't submit the modal in the specified period of time.
            # This is done since Discord doesn't dispatch any event for when a modal is closed/dismissed.
            return

        embed = disnake.Embed(title="Ajout d'une carte")
        for custom_id, value in modal_inter.text_values.items():
            embed.add_field(name=custom_id.capitalize(), value=value, inline=False)
        await modal_inter.response.send_message(embed=embed)


    @commands.slash_command(description="Ajout/Modification d'un responsable de deck ")
    async def update_deck_manager(self, inter: disnake.CommandInteraction, deck_id: int, manager):
        """Ajout/Modification d'un responsable de deck 

        Parameters
        ----------
        deck_id: L'identifiant unique du deck
        manager: <@rôle> ou <@utilisateur> responsable du deck  
        """
        regex_mention = '<@!*&*[0-9]+>'
        is_manager_valid = re.match(regex_mention, manager)

        message = "L'utilisateur  ou le rôle mentionné est incorrect"
        is_ephemeral=True

        if is_manager_valid:

            # Si la mention ressemble à <@!numero_id> => utilisateur avec un nickname
            # Si la mention ressemble à <@numero_id>  => utilisateur
            # Si la mention ressemble à <@&numero_id> => rôle

            if "&" in manager or "!" in manager:
            # Gestion d'erreur à ajouter
                manager_id = int(manager[3:-1])
            else:
                manager_id = int(manager[2:-1])

            is_role_in_guild = inter.guild.get_role(manager_id) is None 
            is_user_in_guild = inter.guild.get_member(manager_id) is None
            
            if is_role_in_guild or is_user_in_guild:
                deck = self.query.get_deck_by_id(deck_id)
                self.query.update_deck_manager(deck_id, manager_id)
                message = f"{manager} a été désigné comme responsable au deck **{deck.deck_name}**"
                is_ephemeral = False
        
        await inter.response.send_message(message, ephemeral=is_ephemeral)

    def confirmation_deck_embed(self, deck_name, deck_id, deck_manager=None):
        
        if(not deck_manager):
            deck_manager="Non défini"
        
        embed = disnake.Embed(title="Création de deck", color=Colour.blue())
        deck_title="__Nom du deck:__"
        deck_value=f"{deck_name}"
        manager_title="__Responsable du dek:__"
        manager_value=f"{deck_manager}"
        help_title="__Commandes utilitaires__"
        help_value=f"__Ajout/Modification du responsable:__\n `/update_deck_manager {deck_id} <@utilisateur>/<@rôle>`\n __Gestion des decks__: `/manage_deck`"

        embed.add_field(name = deck_title,    value = deck_value,inline=False)
        embed.add_field(name = manager_title, value = manager_value,inline=False)
        embed.add_field(name = help_title,    value = help_value,inline=False)
        return embed


    @commands.slash_command(description="Gestionnaire de Promotions")
    async def manage_batches(self, inter: disnake.CommandInteraction):
        """Gestionnaire de Promotions   
        """
        batches_list = self.query.get_batches_list(inter.guild_id)
        view = BatchManagementView(batches_list)

        # Sending a message containing our view
        await inter.send("**Gestion des Promotions:** ", view=view, ephemeral=True)

    @commands.slash_command(description="Gestionnaire de Decks")
    async def manage_decks(self, inter: disnake.CommandInteraction, batch_id:int = None):
        """Menu interactif pour la gestion des Decks 

        Parameters
        ----------
        batch_id: L'identifiant unique de la promotion  
        """
        if batch_id is None:
            print (inter.guild_id)
            batch_id = Query().get_default_batch(inter.guild_id)
            print(batch_id)

        # Create the view containing our dropdown
        deck_list = self.query.get_decks_list(batch_id)
        view = DeckManagementView(deck_list)

        # Sending a message containing our view
        await inter.send("**Gestion des Decks: ** ", view=view, ephemeral=True)

    @commands.slash_command(description="Gestionnaire de Cartes")
    async def manage_cards(self, inter: disnake.CommandInteraction, deck_id):
        """Menu interactif pour la gestion des Decks 

        Parameters
        ----------
        deck_id: L'identifiant unique du deck qui contient les Cartes  
        """
        deck_list = Query().get_cards_list(deck_id)
        view = CardManagementView(deck_list)

        # Sending a message containing our view
        await inter.send("**Gestion des Decks: ** ", view=view, ephemeral=True)


    @commands.slash_command(description="Initialisation du serveur")
    async def initialize(self, inter: disnake.CommandInteraction):
        guild = inter.guild
        # On vérifie si la promo par défaut existe déjà
        if(self.query.is_default_batch_created(guild.id)):
            print(f"Promo déjà crée, suite de l'initialisation")
            await inter.send("Le bot a déjà été initialisé sur le serveur.")
        else:
            # Recherche du premier channel dans lequel on peux poster un message et on le définit comme channel par défaut
            default_channel = None
            for channel in guild.text_channels:
                if channel.permissions_for(guild.me).send_messages:
                    default_channel = channel
                break #breaking so you won't send messages to multiple channels
                        
            # Creation de la promo par défaut
            self.query.create_batch(server_id = guild.id, name = "default", manager = guild.id, member = guild.id, channel=default_channel.id, delay = guild.id)
            print(f"Promo crée avec succès, suite de l'initialisation")
            await inter.send("La promotion a été crée avec succès, le bot est prêt")


def setup(bot : commands.Bot):
    bot.add_cog(SlashCog(bot))