import discord

from discord.ext import commands

import config

from constructors.graphs_constructors import *
from api.api_requests import *

class StatsView(discord.ui.View):
    def __init__(self, client, embeds, statistics):
        super().__init__(timeout=None)
        self.client = client
        self.embeds = embeds
        self.statistics = statistics
        self.graph = None
        self.graph_used = False
        self.graph_url = None
        self.current_embed = embeds[0]
        self.current_embed_number = 0
        self.graph_button_active = True
        self.picture_button_active = True
        self.cross_button_active = False
    
    async def send_message(self, ctx: commands.Context):
        self.set_buttons()
        self.ctx = ctx
        self.message = await ctx.reply(embed = self.current_embed, view = self)
    
    async def update_message(self):
        await self.message.edit(embed = self.current_embed, view = self)
        
    def set_buttons(self):
        if self.current_embed_number == 0:
            self.clear_items()
            self.add_item(self.graph_button)
            self.add_item(self.picture_button)
            self.add_item(self.cross_button)

        elif self.current_embed_number == 1:
            self.clear_items()
            self.add_item(self.previous_button)
            self.add_item(self.next_button)

        else:
            self.clear_items()

        self.add_item(self.my_select)

    def set_embed(self, value):
        if value == '1':
            self.current_embed = self.embeds[0]
            self.current_embed_number = 0
        elif value == '2':
            self.current_embed_number = 1
            if self.previous_button.disabled:
                self.current_embed = self.embeds[1][0]
            else:
                self.current_embed = self.embeds[1][1]
        elif value == '3':
            self.current_embed = self.embeds[2]
            self.current_embed_number = 2
        self.set_buttons()

    async def send_picture(self):
        if self.graph is None:
            self.graph = f_make_graph(
                self.statistics['recent']['elo_change'], 
                self.statistics['recent']['kr_change'],
                self.statistics['recent']['kd_change'],
                self.statistics['recent']['games']
            )
            
        if len(self.statistics['recent']["avatar"]) > 0:
            avatar_link = self.statistics['recent']["avatar"]
        else:
            avatar_link = config.no_avatar_i

        if len(self.statistics['recent']["wall"]) > 0:
            wall_link = self.statistics['recent']["wall"]
        else:
            wall_link = config.no_wall_i

        picture = discord.File(p_fs(self.statistics['recent'], self.graph, [avatar_link, wall_link]), filename='stats.png')

        await self.ctx.send(file = picture, ephemeral = True)

    async def set_graph(self):
        if self.graph is None:
            self.graph = f_make_graph(
                self.statistics['recent']['elo_change'], 
                self.statistics['recent']['kr_change'],
                self.statistics['recent']['kd_change'],
                self.statistics['recent']['games']
            )
        
        if not self.graph_used:
            admin = self.client.get_channel(config.admin_images)
            msg = await admin.send(
                f'{self.ctx.author.name}', 
                file = discord.File(self.graph, filename='graph.png')
            )
            self.graph_url = [i.url for i in msg.attachments][0]
            self.graph_used = True
        
        self.current_embed.set_image(url = self.graph_url)

    @discord.ui.select(options = [
                        discord.SelectOption(label="Last 20 Games", value = '1', description="Shows player's last 20 games statistic"),
                        discord.SelectOption(label="Last Game", value = '2', description="Shows player's last game statistic"),
                        discord.SelectOption(label="Lifetime Statistic", value = '3', description="Shows player's lifetime statistic")
                    ])
    async def my_select(self, interaction: discord.Interaction, option):
        await interaction.response.defer()
        self.set_embed(option.values[0])
        await self.update_message()

    @discord.ui.button(label = 'Graph', custom_id = 'graph', style = discord.ButtonStyle.green, emoji = '📈')
    async def graph_button(self, interaction: discord.Interaction, button):
        await interaction.response.defer()
        self.graph_button.disabled = True
        self.cross_button.disabled = False
        await self.set_graph()
        await self.update_message()

    @discord.ui.button(label = 'Picture', custom_id = 'picture', style = discord.ButtonStyle.green, emoji = '🗒️')
    async def picture_button(self, interaction: discord.Interaction, button):
        await interaction.response.defer()
        self.picture_button.disabled = True
        await self.update_message()
        await self.send_picture()

    @discord.ui.button(label = 'Cross', custom_id = 'cross', style = discord.ButtonStyle.red, emoji='🗑️', disabled=True)
    async def cross_button(self, interaction: discord.Interaction, button):
        await interaction.response.defer()
        self.graph_button.disabled = False
        self.cross_button.disabled = True
        self.current_embed.set_image(url='')
        await self.update_message()

    @discord.ui.button(label = 'Previous', custom_id = 'previous', style = discord.ButtonStyle.green, disabled=True)
    async def previous_button(self, interaction: discord.Interaction, button):
        await interaction.response.defer()
        self.previous_button.disabled = True
        self.next_button.disabled = False
        self.current_embed_number = 1
        self.current_embed = self.embeds[1][0]
        await self.update_message()

    @discord.ui.button(label = 'Next', custom_id = 'next', style = discord.ButtonStyle.green)
    async def next_button(self, interaction: discord.Interaction, button):
        await interaction.response.defer()
        self.previous_button.disabled = False
        self.next_button.disabled = True
        self.current_embed_number = 1
        self.current_embed = self.embeds[1][1]
        await self.update_message()