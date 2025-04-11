import discord
from discord.ext import commands
from discord import app_commands
import discord.ui
import game_info as g_info
import os

class Bot(commands.Bot):
    async def on_ready(self):
        print(f'Logged in as {self.user}')
        try:
            guild_id = discord.Object(id=int(os.getenv('DISCORD_GUILD')))
            synch = await self.tree.sync(guild=guild_id)
            print(synch)
        except Exception as e:
            print(f'Error syncing commands: {e}')

class class_select_view(discord.ui.View):
    def __init__(self):
        super().__init__()
        for i in g_info.game_classes:
            self.add_item(UI_Button(label=g_info.game_classes[i]["name"], style=discord.ButtonStyle.primary, custom_id=i, character=g_info.game_classes[i]))
    
class UI_Button(discord.ui.Button):
    def __init__(self, label: str, style: discord.ButtonStyle, custom_id: str,character):
        super().__init__(label=label, style=style, custom_id=custom_id,emoji=character["icon"])

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"{interaction.user.name} clicked the button with ID: {self.custom_id}", ephemeral=True)