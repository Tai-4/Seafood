import discord

class InteractionResult:
    def __init__(self, response: str):
        self.response = response

    async def call(self, interaction: discord.Interaction):
        await interaction.response.send_message(self.response)

class Success(InteractionResult): pass
class Failure(InteractionResult): pass

