from disnake import Guild
from disnake.ext import commands
from database.query import Query

class EventsCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.query = Query()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Logged in as {self.bot.user} (ID: {self.bot.user.id})")
        print("------")

    @commands.Cog.listener()
    async def on_guild_join(self, guild : Guild):
        
        # On vérifie si la promo par défaut existe déjà
        if(self.query.is_default_batch_created(guild.id)):
            print(f"Promo déjà crée, suite de l'initialisation")
        else:
            # Recherche du premier channel dans lequel on peux poster un message et on le définit comme channel par défaut
            default_channel = None
            for channel in guild.text_channels:
                if channel.permissions_for(guild.me).send_messages:
                    default_channel = channel
                break #breaking so you won't send messages to multiple channels
            
            
            print(guild.id)
            # Creation de la promo par défaut
            self.query.create_batch(server_id = guild.id, name = "default", manager = guild.id, member = guild.id, channel=default_channel.id, delay = guild.id)
            print(f"Promo crée avec succès, suite de l'initialisation")

def setup(bot :commands.Bot):
    bot.add_cog(EventsCog(bot))
