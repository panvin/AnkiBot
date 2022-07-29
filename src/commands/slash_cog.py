from disnake.ext import commands
from  disnake.utils import get
from database.query import Query
from disnake import Colour, Embed, Guild
from settings import db_path
import disnake
import asyncio
import re


class SlashCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.query = Query(db_path)
    
    
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

    @commands.slash_command()
    async def create_card(self, inter: disnake.CommandInteraction):
        # Works same as the above code but using a low level interface.
        # It's recommended to use this if you don't want to increase cache usage.
        await inter.response.send_modal(
            title="Ajout de carte à un deck",
            custom_id="create_card",
            components = [
                disnake.ui.Select(
                    placeholder="Choix du deck",
                    custom_id="deck",
                    min_values=1,
                    max_values=1,
                    options=["Vrai", "Faux"]
                ),
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

    @commands.slash_command()
    async def create_tag_low(self, inter: disnake.CommandInteraction):
        # Works same as the above code but using a low level interface.
        # It's recommended to use this if you don't want to increase cache usage.
        await inter.response.send_modal(
            title="Create Tag",
            custom_id="create_tag_low",
            components=[
                disnake.ui.TextInput(
                    label="Name",
                    placeholder="The name of the tag",
                    custom_id="name",
                    style=disnake.TextInputStyle.short,
                    max_length=50,
                ),
                disnake.ui.TextInput(
                    label="Description",
                    placeholder="The description of the tag",
                    custom_id="description",
                    style=disnake.TextInputStyle.short,
                    min_length=5,
                    max_length=50,
                ),
                disnake.ui.TextInput(
                    label="Content",
                    placeholder="The content of the tag",
                    custom_id="content",
                    style=disnake.TextInputStyle.paragraph,
                    min_length=5,
                    max_length=1024,
                ),
            ],
        )

        # Waits until the user submits the modal.
        try:
            modal_inter: disnake.ModalInteraction = await self.bot.wait_for(
                "modal_submit",
                check=lambda i: i.custom_id == "create_tag_low" and i.author.id == inter.author.id,
                timeout=300,
            )
        except asyncio.TimeoutError:
            # The user didn't submit the modal in the specified period of time.
            # This is done since Discord doesn't dispatch any event for when a modal is closed/dismissed.
            return

        embed = disnake.Embed(title="Tag Creation")
        for custom_id, value in modal_inter.text_values.items():
            embed.add_field(name=custom_id.capitalize(), value=value, inline=False)
        await modal_inter.response.send_message(embed=embed)

###########################################################################################################################

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
                manager_id = manager[3:-1]
            else:
                manager_id = manager[2:-1]

            is_role_in_guild = inter.guild.get_role(manager_id) is None 
            is_user_in_guild = inter.guild.get_member(manager_id) is None
            
            if is_role_in_guild or is_user_in_guild:
                deck = self.query.get_deck_by_id(deck_id)
                self.query.update_deck_manager(deck_id, manager_id)
                message = f"{manager} a été ajouté comme responsable au deck **f{deck.deck_name}**"
                is_ephemeral = False
        
        message = f"`{manager} {manager_id} {is_role_in_guild} {is_user_in_guild}`"
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

def setup(bot : commands.Bot):
    bot.add_cog(SlashCog(bot))