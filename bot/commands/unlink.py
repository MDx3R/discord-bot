import discord

from discord.ext import commands

import config

from api.api_requests import *

async def unlink_body(ctx: commands.Context, member: discord.Member):
    admin_role = ctx.guild.get_role(config.admin_role)
    if admin_role in ctx.author.roles:
        if delete_faceit_linked_user_by_discord_id(member.id) == 200:
            await ctx.reply(f'{member.mention} is unlinked')
        else: 
            await ctx.reply(f"{member.mention} does't have a linked faceit account")
    else:
        await ctx.reply(f"{ctx.author.mention}, you don't have permissions to do that")
