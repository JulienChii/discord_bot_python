import discord
from discord.ext import commands
from discord import app_commands
import discord.ui
import game_info as g_info
import os
import data_manager as dm

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
    def __init__(self, message_id):
        super().__init__()
        print(message_id)
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
            self.add_item(UI_Class_Button(label=g_info.game_classes[i]["name"], style=discord.ButtonStyle.primary, custom_id=i, character=g_info.game_classes[i]))

class UI_Class_Button(discord.ui.Button):
    def __init__(self, label: str, style: discord.ButtonStyle, custom_id: str,character:dict,):
        super().__init__(label=label, style=style, custom_id=custom_id,emoji=character["icon"])

    async def callback(self, interaction: discord.Interaction):
        data = g_info.game_classes[self.label]
        result = dm.insert_character_data(interaction.user.name, character_data=data)
        await interaction.response.send_message(result, ephemeral=True)



class UI_Playerinfo(discord.ui.View):
    def __init__(self, message_id):
        super().__init__()
        print(message_id)
        embed = discord.Embed(
            color=discord.Color.pink(),
            title="Profile Information",
            description=""
        )
        info = dm.get_player_info(message_id.user.name)
        print(info)
        if info is int:
            embed.description = "No character found!"
            self.embed = embed
            return
        elif len(info) == 0:
            embed.description = "No character found!"
        else:
            embed.add_field(name="**Name**", value=info[0][1], inline=False)
            embed.add_field(name="**Class**", value=info[0][2], inline=False)
            embed.add_field(name="**Attack**", value=info[0][3], inline=False)
            embed.add_field(name="**Defense**", value=info[0][4], inline=False)
        self.embed = embed