from disnake.ext import commands
from disnake import Colour, Embed
from views.ephemeral_counter import EphemeralCounter
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

    @commands.command()
    async def counter(self, ctx: commands.Context):
        """Starts a counter for pressing."""
        await ctx.send("Press!", view=EphemeralCounter())

    @commands.command(description="Affichage de l'aide")
    async def help(self, ctx):
        command_string= """`?add chiffre chiffre`:\tAjoute deux nombres\n
                        `?choose choix1 choix2 ...`:\tRetounre une réponse parmi les multiples choix\n
                        `?help`:\tAffiche la liste des commandes"""
        
        
        embed = Embed(title="Liste des commandes disponibles", color=Colour.blue())
        embed.add_field(name="Commandes", value=command_string, inline=False)

        await ctx.send(embed=embed)

def setup(bot :commands.Bot):
    bot.add_cog(MessageCog(bot))
