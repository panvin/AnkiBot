import disnake
from views.counter import Counter

# Define a View that will give us our own personal counter button
class EphemeralCounter(disnake.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    # When this button is pressed, it will respond with a Counter view that will
    # give the button presser their own personal button they can press 5 times.
    @disnake.ui.button(label="Click", style=disnake.ButtonStyle.blurple)
    async def receive(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        # ephemeral=True makes the message hidden from everyone except the button presser
        await interaction.response.send_message("Enjoy!", view=Counter(), ephemeral=True)