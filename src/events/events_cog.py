from disnake import Guild
from disnake.ext import commands, tasks
from ankigen import AnkiGenerator, BatchGenerator
from database.query import Query

class EventsCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.query = Query()
        self.decks_to_update = []
        self.batch_id_to_update = []
        #self.generate_file.start()

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

    @tasks.loop(hours = 3)
    async def generate_file(self):
        ankigen = AnkiGenerator(self.decks_to_update)
        ankigen.generate_deck()
        ankigen.generate_files()
        batch_gen = BatchGenerator(self.batch_id_to_update) 
        batch_gen.generate_batch_archive()
    
    @generate_file.before_loop
    async def fill_list_to_update(self):
        self.decks_to_update = self.query.get_decks_to_update()
        for deck in self.decks_to_update:
            self.batch_id_to_update.append(deck.batch_id)

    @generate_file.after_loop
    async def reset_list_to_update(self):
        self.decks_to_update = []
        self.batch_id_to_update = []


def setup(bot :commands.Bot):
    bot.add_cog(EventsCog(bot))
