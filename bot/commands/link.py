import discord

from discord.utils import get

import config
from discord.ext import commands

from constructors.embeds_constructor import *
from constructors.graphs_constructors import *
from api.api_requests import *

async def link_body(ctx: commands.Context, name):
    if name is not None:
        await ctx.defer(ephemeral = False)
        if ctx.channel.id == int(config.link_channel):
            if get_faceit_linked_user_by_discord_id(ctx.author.id) is None:
                if get_faceit_linked_user_by_faceit_nickname(name) is None:

                    #make it embeded
                    await ctx.send(f'{ctx.author.mention}, wait 10-20 seconds, please', delete_after = 10.0)

                    instance = get_faceit_user_by_nickname(name)
                    if instance is None:
                        instance = post_faceit_user_by_nickname(name)

                    if instance is not None:
                        if instance['stats'] != 0:

                            post_discord_user(ctx.author.id)
                            post_faceit_linked_user(ctx.author.id, instance['id'])

                            role = get(ctx.author.guild.roles, id = int(config.member_role))
                            author = get(ctx.author.guild.members, id = ctx.author.id)
                            
                            await author.add_roles(role)

                        else:
                            message = await ctx.reply(f"{ctx.author.mention}, you can't link account with no games played. Play some (atleast 1) or check your account name again: {name}", mention_author=True, ephemeral=True)
                            await message.delete(delay=10.0)

                else:
                    id_holder = get_faceit_linked_user_by_faceit_nickname(name)['discord_id']

                    link_error = discord.Embed(title = f'ID {name} is already linked', 
                        description = f'''**ID holder: <@{id_holder}>**
                        If this ID ({name}) belongs to you, use !unlink here to transfer it to you.''', 
                        colour = config.error
                    )

                    await ctx.send(embed = link_error, delete_after = 30.0)

            else:
                await ctx.send(f"{ctx.author.mention}, you have already linked account", delete_after = 10.0)
                await ctx.message.delete()

        else:
            await ctx.send(f"{ctx.author.mention}, you can't use it here", delete_after = 10.0)
            await ctx.message.delete()

    else:   
        await ctx.send(f"{ctx.author.mention}, you can't link nothing", delete_after = 15.0)
        await ctx.message.delete()    