import asyncio
import discord
from discord.ext import commands
from discord import app_commands
import discord.ui
import os
import logging
from dotenv import load_dotenv as ld
import global_classes as cls
import data_manager as dm
import game_runtime as g_runtime

ld()

intents  = discord.Intents.default()
intents.message_content = True
bot = cls.Bot(command_prefix='!', intents=intents)
guild_id = discord.Object(id= int(os.getenv('DISCORD_GUILD')))

##___________Commands___________##

# This command will be used to create a character for the user #
@bot.tree.command(name="create_character", description="Create your Character", guild=guild_id)
async def create_character(interaction: discord.Interaction):
    ui = cls.UI_Create_Character(message_id=interaction.message)
    await interaction.response.send_message("", ephemeral=True,view=ui,embed=ui.embed)

#Character Info Command
@bot.tree.command(name="me", description="See your Character Stats", guild=guild_id)
async def me(interaction: discord.Interaction, public:bool = False):
    print(interaction.user.name)
    char_info = cls.UI_Playerinfo(message_id=interaction)
    await interaction.response.send_message("", ephemeral=not public,view=char_info,embed=char_info.embed)

# Adventure Command
@bot.tree.command(name="adventure", description="Start an adventure to gather ressources and Gold.", guild=guild_id)
async def adventure(interaction: discord.Interaction):
    result = g_runtime.get_adventure(interaction.user.name)
    if result == None:
        adventure = cls.UI_Select_Adventure(message_id=interaction)
        await interaction.response.send_message("", ephemeral=True,view=adventure,embed=adventure.embed)
    else:
        await interaction.response.send_message(f"Adventure already running for player: {interaction.user.name} with a remaining time of: {round(abs(result))} seconds.", ephemeral=True)

##___________Events___________##

@bot.event
async def on_ready():
    bot.loop.create_task(update_adventure_list())


async def update_adventure_list():
    while True:
        g_runtime.update_adventure_list()
        await asyncio.sleep(1) # Update every second

bot.run(os.getenv('DISCORD_TOKEN'))