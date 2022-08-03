import disnake
from disnake.ext import commands
from settings import my_discord_token
from settings import test_guild

intents = disnake.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("?"),     #   Trigger du bot
    description=None,                                   #   Description pour l'aide par défaut
    intents=intents,                                    #   Intents du bot
    test_guilds=[test_guild],                           #   Serveur par défaut pour le test de commande. Pour synchro globale il faut ne rien renseigner
    sync_commands_debug=True,                           #   Par défaut False. Permet de voir l'état de synchro des commandes /
    help_command=None                                   #   On désactive l'aide par défaut et on crée la notre
)

bot.load_extension('events.slash_cog')
bot.load_extension('events.commands_cog')
bot.load_extension('events.events_cog')

bot.run(my_discord_token)