from disnake.ext import commands
from database.query import Query
import disnake
import re


class RoleCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    #@commands.has_permissions(disnake.Permissions.administrator == True)
    @commands.slash_command(description="Ajout/Modification d'un responsable de Promotion")
    async def update_batch_manager(self, inter: disnake.CommandInteraction, batch_id: int, manager):
        """Ajout/Modification d'un responsable de Promotion 

        Parameters
        ----------
        batch_id: L'identifiant unique de la promotion
        manager: <@rôle> ou <@utilisateur> responsable de la Promotion 
        """
        if self.is_new_mention_valid_and_in_server(manager, inter.guild):
            batch = Query().get_batch_by_id(batch_id)
            Query().update_batch_manager(batch_id, self.get_id_from_mention(manager))
            message = f"{manager} a été désigné comme responsable au deck **{batch.batch_name}**"
        else:
            message = "L'utilisateur  ou le rôle mentionné est incorrect"
        
        await inter.response.send_message(message, ephemeral=True)

    @commands.slash_command(description="Ajout/Modification d'un responsable de Deck")
    async def update_deck_manager(self, inter: disnake.CommandInteraction, deck_id: int, manager):
        """Ajout/Modification d'un responsable de Deck 

        Parameters
        ----------
        deck_id: L'identifiant unique du deck
        manager: <@rôle> ou <@utilisateur> responsable du deck  
        """
        if self.is_new_mention_valid_and_in_server(manager, inter.guild):
            deck = Query().get_deck_by_id(deck_id)
            Query().update_batch_manager(deck_id, self.get_id_from_mention(manager))
            message = f"{manager} a été désigné comme responsable au deck **{deck.deck_name}**"
        else:
            message = "L'utilisateur  ou le rôle mentionné est incorrect"
        
        await inter.response.send_message(message, ephemeral=True)

    @commands.slash_command(description="Ajout/Modification d'un responsable de Promotion")
    async def update_batch_member(self, inter: disnake.CommandInteraction, batch_id: int, member):
        """Ajout/Modification d'un responsable de Promotion 

        Parameters
        ----------
        batch_id: L'identifiant unique du deck
        member: <@rôle> des membres ayant accès a la promotion et aux deck associés 
        """

        message = "L'utilisateur  ou le rôle mentionné est incorrect"
        is_ephemeral=True

        if self.is_new_mention_valid_and_in_server(member, inter.guild):
            batch = Query().get_batch_by_id(batch_id)
            Query().update_batch_manager(batch_id, member)
            message = f"{member} a maintenant accès aux deck: **{batch.batch_name}**"
        else:
            message = "L'utilisateur  ou le rôle mentionné est incorrect"
        
        await inter.response.send_message(message, ephemeral=is_ephemeral)

    def is_mention_valid(self, mention :str):
        regex_mention = '<@!*&*[0-9]+>'
        return re.match(regex_mention, mention)

    def get_id_from_mention(self, mention :str):
        # Si la mention ressemble à <@!numero_id> => utilisateur avec un nickname
            # Si la mention ressemble à <@numero_id>  => utilisateur
            # Si la mention ressemble à <@&numero_id> => rôle

            if "&" in mention or "!" in mention:
            # Gestion d'erreur à ajouter
                return int(mention[3:-1])
            else:
                return int(mention[2:-1])
    
    def is_role_or_user_in_guild(self, id: int, guild :disnake.Guild):
        is_role_in_guild = guild.get_role(id) is not None 
        is_user_in_guild = guild.get_member(id) is not None
        return is_role_in_guild or is_user_in_guild

    def is_new_mention_valid_and_in_server(self, mention: str, guild : disnake.Guild):
        if self.is_mention_valid(mention):
            mention_id = self.get_id_from_mention(mention)
            
            if self.is_role_or_user_in_guild(mention_id, guild):
                return True
        return False


def setup(bot : commands.Bot):
    bot.add_cog(RoleCog(bot))