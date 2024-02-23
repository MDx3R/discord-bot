import discord
import logging
import datetime
import sqlite3
from discord.interactions import Interaction
import requests
import asyncio

from discord.ui import Button, View, Select
from discord import utils, ui
from discord import app_commands
from discord.ext import commands, tasks
from discord.utils import get

import config

from constructors.embeds_constructor import *
from constructors.graphs_constructors import *
from api.api_requests import *
from commands.on_ready import on_ready_body
from commands.link import link_body
from commands.stats import stats_body
from commands.refresh import refresh_body, refresh_error_body
from commands.unlink import unlink_body

client = commands.Bot(command_prefix='!', intents = discord.Intents.all())

@client.event
async def on_ready():
    await on_ready_body(client)

@client.hybrid_command(name = "link", with_app_command = True, description = "Testing")
@app_commands.guilds(discord.Object(id = config.guild_id))
@app_commands.describe(name = 'write down your faceit account name')
async def link(ctx: commands.Context, name):
    await link_body(ctx, name)

@client.hybrid_command(name = "stats", with_app_command = True, description = "Testing")
@app_commands.guilds(discord.Object(id = config.guild_id))
@app_commands.describe(user = 'Leave it empty, mention someone or write down a faceit nickname')
async def stats(ctx: commands.Context, user = None):
    await stats_body(client, ctx, user)

@client.hybrid_command(name = "refresh", description = "Testing")
@app_commands.guilds(discord.Object(id = config.guild_id))
@app_commands.checks.cooldown(1, 3600.0, key=lambda i: (i.guild_id, i.user.id, i.channel_id))
async def refresh(ctx: commands.Context):
    await refresh_body(ctx)

@refresh.error
async def on_refresh_error(ctx: commands.Context, error: app_commands.AppCommandError):
    await refresh_error_body(ctx, error)

@client.command(name='unlink')
async def unlink(ctx: commands.Context, member: discord.Member):
    await unlink_body(ctx, member)

client.run(config.TOKEN)