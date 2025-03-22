import os
import discord
from typing import Any, Optional
from discord import VoiceClient
from discord import app_commands
from discord.flags import Intents
from interaction_result import Failure, InteractionResult, Success

class Seafood(discord.Client):
    def __init__(self, *, intents: Intents, **options: Any) -> None:
        super().__init__(intents=intents, **options)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await client.tree.sync()

    def is_connecting_to_user_vc(self, user) -> bool:
        if user.voice is None: return False
        return any(c for c in self.voice_clients if c.channel == user.voice.channel)

    def find_connecting_user_voice_client(self, user) -> Optional[VoiceClient]:
        if user.voice is None: return None
        return next((c for c in self.voice_clients if c.channel == user.voice.channel), None)

    async def connect_to_vc(self, interaction: discord.Interaction) -> InteractionResult:
        if interaction.user.voice is None:
            return Failure("ボイスチャンネルに接続してください。")
        if self.is_connecting_to_user_vc(interaction.user):
            return Failure("すでにボイスチャンネルに接続しています。")

        await interaction.user.voice.channel.connect()
        return Success("接続に成功しました。")

    async def disconnect_from_vc(self, interaction: discord.Interaction) -> InteractionResult:
        try:
            user_voice_client = self.find_connecting_user_voice_client(interaction.user)
            if user_voice_client is None:
                return Failure("ボイスチャットに接続していません。")
        except StopIteration:
            return Failure("ボイスチャットに接続していません。")
        await user_voice_client.voice_disconnect()
        return Success("ボイスチャットから切断しました。")

intents = discord.Intents.default()
client = Seafood(intents=intents)

@client.tree.command(name="c")
async def connect_to_vc(interaction: discord.Interaction):
    result = await client.connect_to_vc(interaction)
    await result.call(interaction)

@client.tree.command(name="dc")
async def disconnect_from_vc(interaction: discord.Interaction):
    result = await client.disconnect_from_vc(interaction)
    await result.call(interaction)

@client.tree.command(name="play")
async def play(interaction: discord.Interaction, play: str):
    if interaction.user.voice is None:
        await client.connect_to_vc(interaction)
    if not os.path.isfile("../res/" + play):
        await Failure("ファイル `" + play + "` は見つかりませんでした。").call(interaction)
        return
    if not client.is_connecting_to_user_vc(interaction.user):
        await Failure("同じボイスチャットに接続してください。").call(interaction)
        return

    try:
        interaction.guild.voice_client.play(
            discord.FFmpegPCMAudio("../res/" + play)
        )
    except Exception:
        await interaction.response.send_message("再生に失敗しました。")
        raise
    await interaction.response.send_message("再生を開始しました。")
