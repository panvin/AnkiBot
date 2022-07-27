from disnake.ext import commands
import disnake
import asyncio

class SlashCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    
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

def setup(bot):
    bot.add_cog(SlashCog(bot))