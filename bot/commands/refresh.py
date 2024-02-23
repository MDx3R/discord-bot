import discord

from discord import app_commands
from discord.ext import commands

import config

from api.api_requests import *

async def refresh_body(ctx: commands.Context):
    await ctx.defer(ephemeral = True)
    if ctx.channel.id == config.vip_stats:
        faceit_id = get_faceit_linked_user_by_discord_id(ctx.author.id)['faceit_id']
        if faceit_id is not None:

            patch_faceit_user_by_id(faceit_id)

            await ctx.reply(f"Stats is successfully refreshed", delete_after=10.0, ephemeral = True)
    else:
        await ctx.reply(f"{ctx.author.mention}, you can't use it here", delete_after = 10.0, ephemeral = True)

async def refresh_error_body(ctx: commands.Context, error: app_commands.AppCommandError):
    if not isinstance(error, discord.NotFound):
        length = ''.join([i for i in str(error) if i.isdigit()])
        length = round(int(length)/100)
        min = length//60
        sec = length%60
        await ctx.reply(f'Cooldown: {min}m {sec}s', delete_after = 10.0, ephemeral = True)