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

class UI_Create_Character(discord.ui.View):
    def __init__(self):
        super().__init__()
        embed = discord.Embed(
            color=discord.Color.blue(),
            title="Create your Character",
            description="Pick one of the Classes for your Character."
        )
        for i in g_info.game_classes:
            embed.add_field(name=f"{g_info.game_classes[i]["name"]} | {g_info.game_classes[i]["icon"]}" , value=" ", inline=False)
            embed.add_field(name=f"Description" , value=f"{g_info.game_classes[i]["description"]}", inline=False)
            embed.add_field(name=f"------------------------------" , value=" ", inline=False)
        self.embed = embed

        for i in g_info.game_classes:
            self.add_item(UI_Button(label=g_info.game_classes[i]["name"], style=discord.ButtonStyle.primary, custom_id=i, character=g_info.game_classes[i]))

class UI_Button(discord.ui.Button):
    def __init__(self, label: str, style: discord.ButtonStyle, custom_id: str,character):
        super().__init__(label=label, style=style, custom_id=custom_id,emoji=character["icon"])

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"{interaction.user.name} clicked the button with ID: {self.custom_id}", ephemeral=True)

       
