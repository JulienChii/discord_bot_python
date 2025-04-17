import discord
from discord.ext import commands
from discord import app_commands
import discord.ui
import game_info as g_info
import os
import data_manager as dm
import game_runtime as g_runtime

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

class UI_Adventure_Button(discord.ui.Button):
    adventure_id = ""
    req_time = 0
    def __init__(self, label: str, style: discord.ButtonStyle, custom_id: str, required_time:int = 10):
        self.adventure_id = custom_id
        self.req_time = required_time
        super().__init__(label=label, style=style, custom_id=custom_id)

    async def callback(self, interaction: discord.Interaction):
        result = g_runtime.set_adventure(interaction.user.name,adventure=self.adventure_id,required_time=self.req_time)
        if result:
            await interaction.response.send_message(f"Adventure started for player: {interaction.user.name} Adventure ID: {self.adventure_id}", ephemeral=True)
        else:
            await interaction.response.send_message(f"Adventure already running for player: {interaction.user.name} Adventure ID: {self.adventure_id}", ephemeral=True)

class UI_Playerinfo(discord.ui.View):
    def __init__(self, message_id):
        super().__init__()
        embed = discord.Embed(
            color=discord.Color.pink(),
            title="Profile Information",
            description=""
        )
        info = dm.get_player_info(message_id.user.name)
        if info is int:
            embed.description = "No character found!"
            return
        elif len(info) == 0:
            embed.description = "No character found!"
        else:
            embed.add_field(name="**Name**", value=info[0][1], inline=False)
            embed.add_field(name="**Class**", value=info[0][2], inline=False)
            embed.add_field(name="**Attack**", value=info[0][3], inline=False)
            embed.add_field(name="**Defense**", value=info[0][4], inline=False)
        self.embed = embed

class UI_Select_Adventure(discord.ui.View):
    def __init__(self, message_id):
        super().__init__()
        embed = discord.Embed(
            color=discord.Color.red(),
            title="Starting an Adventure",
            description=""
        )
        self.add_item(UI_Adventure_Button(label="***Adventure 1***", style=discord.ButtonStyle.primary, custom_id="adventure 1", required_time=5))
        self.add_item(UI_Adventure_Button(label="***Adventure 2***", style=discord.ButtonStyle.primary, custom_id="adventure 2",required_time=30))
        self.add_item(UI_Adventure_Button(label="***Adventure 3***", style=discord.ButtonStyle.primary, custom_id="adventure 3", required_time=10))
        
        embed.add_field(name="**Select a Adventure**", value="")
        embed.add_field(name="**Adventure 1**", value=" ", inline=False)
        embed.add_field(name="Description1",value="", inline=False)
        embed.add_field(name="**Adventure 2**", value=" ", inline=False)
        embed.add_field(name="Description2",value="", inline=False)
        embed.add_field(name="**Adventure 3**", value=" ", inline=False)
        embed.add_field(name="Description3",value="", inline=False)
        self.embed = embed