from disnake.ext import commands
from disnake import Colour, Embed
from database.query import Query
from views.deck_management import DeckManagementView
import random

class MessageCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command()
    async def add(self, ctx, left: int, right: int):
        """Adds two numbers together."""
        await ctx.send(left + right)

    @commands.command()
    async def choose(self, ctx, *choices: str):
        """Chooses between multiple choices."""
        await ctx.send(random.choice(choices))

    @commands.command(description="Affichage de l'aide")
    async def help(self, ctx):
        command_string= """`?add chiffre chiffre`:\tAjoute deux nombres\n
                        `?choose choix1 choix2 ...`:\tRetounre une réponse parmi les multiples choix\n
                        `?help`:\tAffiche la liste des commandes"""
        
        
        embed = Embed(title="Liste des commandes disponibles", color=Colour.blue())
        embed.add_field(name="Commandes", value=command_string, inline=False)

        await ctx.send(embed=embed)

    ########################################################################

    @commands.slash_command()
    async def _manage_decks(self, ctx, batch_id:int = None):
        """Menu interactif pour la gestion des Decks 

        Parameters
        ----------
        batch_id: L'identifiant unique de la promotion  
        """
        if batch_id is None:
            print (ctx.bot.guild.id)
            batch_id = Query().get_default_batch(ctx.bot.guild.id)
            print(batch_id)

        # Create the view containing our dropdown
        deck_list = Query().get_decks_list(batch_id)
        view = DeckManagementView(deck_list)

        # Sending a message containing our view
        await ctx.send("**Gestion des Decks: ** ", view=view, ephemeral=True)

def setup(bot :commands.Bot):
    bot.add_cog(MessageCog(bot))
