import disnake

class Dropdown(disnake.ui.Select):
    def __init__(self, text):

        # Set the options that will be presented inside the dropdown
        options = [
            disnake.SelectOption(
                label=text[0], description="Your favourite colour is red", emoji="🟥"
            ),
            disnake.SelectOption(
                label=text[1], description="Your favourite colour is green", emoji="🟩"
            ),
            disnake.SelectOption(
                label=text[2], description="Your favourite colour is blue", emoji="🟦"
            ),
        ]

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(
            placeholder="Choose your favourite colour...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: disnake.MessageInteraction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.
        await interaction.response.send_message(f"Your favourite colour is {self.values[0]}")