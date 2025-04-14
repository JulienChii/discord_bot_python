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

## ___________Commands___________ ##

#Ping Command
@bot.tree.command(name="ping", description="Ping the bot", guild=guild_id)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!", ephemeral=True,)
    await interaction.message.delete(delay=5)

# This command will be used to create a character for the user
@bot.tree.command(name="create_character", description="Create your Character", guild=guild_id)
async def ping(interaction: discord.Interaction):
    ui = cls.UI_Create_Character(message_id=interaction.message)
    await interaction.response.send_message("result", ephemeral=True,view=ui,embed=ui.embed)

#Character Info Command
@bot.tree.command(name="me", description="See your Character Stats", guild=guild_id)
async def ping(interaction: discord.Interaction, public:bool = False):
    await interaction.response.send_message("This is a Test", ephemeral=not public)



bot.run(os.getenv('DISCORD_TOKEN'))