import discord
from discord.ext import commands
from discord import app_commands
import discord.ui
import os
import logging
from dotenv import load_dotenv as ld
import global_classes as cls
ld()

intents  = discord.Intents.default()
intents.message_content = True
bot = cls.Bot(command_prefix='!', intents=intents)
guild_id = discord.Object(id=int(os.getenv('DISCORD_GUILD')))

## ___________Commands___________ ##

#Ping-Command
@bot.tree.command(name="ping", description="Ping the bot", guild=guild_id)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!", ephemeral=True, view=cls.class_select_view())




bot.run(os.getenv('DISCORD_TOKEN'))