#import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageFont, ImageDraw
import config
from io import BytesIO
import requests

def f_make_graph(elo, kr, kd, games):
    elo = list(reversed(elo))
    kr = list(reversed(kr))
    kd = list(reversed(kd))

    game_list = [i for i in range(1, games+1)]
    fig, ax1= plt.subplots(figsize=(8, 4.5))
    ax2 = ax1.twinx()
    ax1.set_frame_on(False)
    ax2.set_frame_on(False)
    ax2.set_xticks

    #elo
    ax2.plot(game_list, elo, color='#fc5700', marker='.', markersize=7)
    ax2.tick_params(
        axis='both',
        which='both', 
        bottom=False,
        top=False,
        left=False,
        right=False,
        labelcolor = '#ffffff',
        labelbottom=True,
        labelright=False,
        labelleft=True)
    
    ax2.set_yticks(elo)

    #kr, kd
    ax1.plot(game_list, kd, color='green', marker='.', markersize=7)
    ax1.plot(game_list, kr, color='#489aff', marker='.', markersize=7)
    ax1.tick_params(
        axis='both',
        which='both', 
        bottom=False,
        top=False,
        left=False,
        right=False,
        labelcolor = '#ffffff',
        labelleft=False,
        labeltop=False,
        labelright=True,
        labelbottom=True)
    ax1.set_xticks(range(1, games+1))

    #saving
    return fig2img(fig)

import io

def fig2img(fig):
    buf = io.BytesIO()
    fig.savefig(buf, transparent = True)
    buf.seek(0)
    return buf

def p_fs(stats, graph, links):
    #samples
    im = Image.open('resources/png4.png')
    name_font = ImageFont.truetype('resources/font1.ttf', size=26)
    elo_font = ImageFont.truetype('resources/font1.ttf', size=17)
    stats_font = ImageFont.truetype('resources/font1.ttf', size=35)
    score_font = ImageFont.truetype('resources/font1.ttf', size=72)
    red_line = Image.open('resources/red_line.png')
    green_line = Image.open('resources/green_line.png')

    #data
    lvls_id = config.lvls_id
    games = stats['games']
    elo = stats['elo_change']
    kr = stats['kr_change']
    kd = stats['kd_change']

    #files
    lvl = Image.open(f'resources/{lvls_id[stats["lvl"]]}.png')

    #resizing
    lvl = lvl.resize((100, 100))

    #allows drawing
    d = ImageDraw.Draw(im, 'RGBA')

    #avatar
    if links[0] != config.no_avatar_i:
        response = requests.get(links[0])
        avatar = Image.open(BytesIO(response.content))
        avatar = avatar.resize((196, 196))
        im.paste(avatar, (44, 255))
    else:
        avatar = Image.open('resources/no_avatar.png')
        im.paste(avatar, (44, 255), mask=avatar)

    #wall
    if links[1] != config.no_wall_i:
        response = requests.get(links[1])
        wall = Image.open(BytesIO(response.content))
        wall = wall.resize((790, 209))
        im.paste(wall, (44, 32))
    else:
        wall = Image.open('resources/no_wall.png')
        im.paste(wall, (44, 32), mask=wall)

    #lvl
    im.paste(lvl, (487, 290), mask = lvl)

    #name
    d.text(
            (812, 275),
            stats['name'],
            font=name_font,
            anchor='rm',
            fill='#ffffff')
    
    #wins
    d.text(
            (427-130, 402),
            f'wins: {stats["stats"]["wins"]}',
            font=stats_font,
            anchor='lm',
            fill='#ffffff')

    #loses
    d.text(
            (778, 402),
            f'loses: {stats["stats"]["loses"]}',
            font=stats_font,
            anchor='rm',
            fill='#ffffff')

    #elo
    d.text(
            (537, 414),
            f'{stats["elo"]} elo',
            font=elo_font,
            anchor='ms',
            fill='#ffffff')

    #winrate #ближе к надписи
    d.text(
            (414-28, 285),
            f'{stats["stats"]["winrate"]}%',
            font=elo_font,
            anchor='ms',
            fill='#ffffff')

    #kills
    d.text(
        (452, 477),
        f'{stats["stats"]["kills"]}',
        font=stats_font,
        fill='#ffffff')

    #kr 
    d.text(
        (452, 477+49),
        f'{stats["stats"]["kr"]}',
        font=stats_font,
        fill='#ffffff')

    #hs
    d.text(
        (452, 477+98),
        f'{stats["stats"]["hs"]}%',
        font=stats_font,
        fill='#ffffff')

    #deaths
    d.text(
        (452+269, 477),
        f'{stats["stats"]["deaths"]}',
        font=stats_font,
        fill='#ffffff')

    #kd
    d.text(
        (452+269, 477+49),
        f'{stats["stats"]["kd"]}',
        font=stats_font,
        fill='#ffffff')

    #assists
    d.text(
        (452+269, 477+98),
        f'{stats["stats"]["assists"]}',
        font=stats_font,
        fill='#ffffff')

    #lines
    green_line = green_line.resize((24*20, 18))
    im.paste(green_line, (777-480, 442-18, 777, 442))

    l_num = stats["stats"]["loses"]
    if l_num > 0:
        red_line = red_line.resize((24*l_num, 18))
        im.paste(red_line, (777-24*l_num, 442-18, 777, 442))

    #graph
    graph = Image.open(graph)
    im.paste(graph, (-16+51, 614+3), mask = graph)

    buf = io.BytesIO()
    im.save(buf, format='PNG')
    buf.seek(0)

    return buf