import discord

import config

async def on_ready_body(client):
    synced = await client.tree.sync(guild = discord.Object(id = config.guild_id))

    logs = client.get_channel(config.admin_invite_logs)
    await logs.purge()

    images = client.get_channel(config.admin_images)
    await images.purge()

    print('client connected')