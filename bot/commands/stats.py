import discord

from discord.ext import commands

import config

from constructors.embeds_constructor import *
from api.api_requests import *
from views.stats_view import StatsView

async def stats_body(client, ctx: commands.Context, user = None):
    if ctx.channel.id == config.vip_stats:
        await ctx.defer(ephemeral = False)

        if user is None: #stats без указания пользователя
            all_stats = get_faceit_user_by_id(get_faceit_linked_user_by_discord_id(ctx.author.id)['faceit_id'])
        elif type(user) is str:
            if str(i for i in user[2:-1] if i.isdigit()) == user[2:-1]:
                if (x := get_faceit_linked_user_by_discord_id(user[2:-1])) is not None: #stats с упоминанием пользователя
                    all_stats = get_faceit_user_by_id(x['faceit_id'])
            else: #stats с никнеймом пользователя на faceit
               all_stats = get_faceit_user_by_nickname(user)
               if all_stats is None:
                   all_stats = post_faceit_user_by_nickname(user)

        if all_stats is not None:
            all_stats = all_stats['stats']
            recent = all_stats['recent']
            last = all_stats['last']
            lifetime = all_stats['lifetime']

            steam_id = recent['steam_id']
            nickname = recent['name']
            if steam_id != 0:
                des = f"[Faceit](https://faceit.com/en/players/{nickname}) [Steam](https://steamcommunity.com/profiles/{steam_id})"
            else:
                des = f"[Faceit](https://faceit.com/en/players/{nickname})"

            embeds = [
                recent_stats_embed(recent, des), 
                [last_game_page_1_embed(last), last_game_page_2_embed(last)], 
                lifetime_stats_embed(lifetime, des)
            ]

            view = StatsView(client, embeds, all_stats)

            await view.send_message(ctx)

        else:
            message = await ctx.reply(f"{ctx.author.mention}, no record in database.", mention_author=True, ephemeral=True)
            await message.delete(delay=10.0)