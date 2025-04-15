import discord
from discord.ext import commands
from discord import app_commands
import discord.ui
import os
import logging
from dotenv import load_dotenv as ld
import global_classes as cls
import data_manager as dm

ld()

intents  = discord.Intents.default()
intents.message_content = True
bot = cls.Bot(command_prefix='!', intents=intents)
guild_id = discord.Object(id= int(os.getenv('DISCORD_GUILD')))

##___________Commands___________##

# This command will be used to create a character for the user #
@bot.tree.command(name="create_character", description="Create your Character", guild=guild_id)
async def ping(interaction: discord.Interaction):
    ui = cls.UI_Create_Character(message_id=interaction.message)
    await interaction.response.send_message("", ephemeral=True,view=ui,embed=ui.embed)

#Character Info Command
@bot.tree.command(name="me", description="See your Character Stats", guild=guild_id)
async def ping(interaction: discord.Interaction, public:bool = False):
    print(interaction.user.name)
    char_info = cls.UI_Playerinfo(message_id=interaction)
    await interaction.response.send_message("", ephemeral=not public,view=char_info,embed=char_info.embed)




bot.run(os.getenv('DISCORD_TOKEN'))