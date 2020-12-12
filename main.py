import discord
from discord.ext import commands

CLIENT = discord.Client()

bot = commands.Bot(command_prefix="!", description="Testing this thing")