from disnake.ext import commands
from disnake import Colour, Embed
import random

from ankigen import AnkiGenerator, BatchGenerator
from database.query import Query

class MessageCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.query = Query()
    
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

    @commands.command()
    async def generate_file(self, ctx):
        decks_to_update = []
        batch_id_to_update = []
        decks_to_update = self.query.get_decks_to_update()
        for deck in decks_to_update:
            batch_id_to_update.append(deck.batch_id)
        ankigen = AnkiGenerator(decks_to_update)
        ankigen.generate_deck()
        ankigen.generate_files()
        batch_gen = BatchGenerator(batch_id_to_update) 
        batch_gen.generate_batch_archive()

def setup(bot :commands.Bot):
    bot.add_cog(MessageCog(bot))
