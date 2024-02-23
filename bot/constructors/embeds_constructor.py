import config
import datetime
import discord

def recent_stats_embed(stats, description):
    #main data
    name = stats['name']
    avatar = stats['avatar']
    elo = stats['elo']
    lvl = stats['lvl']

    #stats
    kills = stats['stats']['kills']
    deaths = stats['stats']['deaths']
    #assists = stats['stats']['assists']
    kr = stats['stats']['kr']
    hs = stats['stats']['hs%']
    kd = stats['stats']['kd']
    winrate = int(stats['stats']['winrate'])
    wins = stats['stats']['wins']
    loses = stats['stats']['loses']

    #getting the rest
    lvl_emoji = config.lvls[int(lvl)]

    #winrate line
    green_line = config.green_line
    red_line = config.red_line

    greenSquare = round(winrate/8.33)
    redSquare = 12 - greenSquare
    winrate_line = ''.replace('', green_line*greenSquare, 1) + ''.replace('', red_line*redSquare, 1)

    embed_dict = {
        "title": f"Recent Competitive Stats",
        "description": f'{description}',
        "color": 0x4899FF,
        "timestamp": datetime.datetime.now().isoformat(),
        "author": {
            "name": f'{name}',
            "icon_url": f'{avatar}',
        },
        "thumbnail": {"url": f'{avatar}'},
        "fields": [
            {"name": "KRR", "value": f'```yaml\n{kr}```', "inline": "true"},
            {"name": "KDR", "value": f'```yaml\n{kd}```', "inline": "true"},
            {"name": f"Rating <{lvl_emoji}>", "value": f'```yaml\n{elo}```', "inline": "true"},
            {"name": "Avg Kills", "value": f'```yaml\n{kills}```', "inline": "true"},
            {"name": "Avg Deaths", "value": f'```yaml\n{deaths}```', "inline": "true"},
            {"name": "Avg HS", "value": f'```yaml\n{hs}%```', "inline": "true"},
            {"name": f"Winrate - {winrate}%", "value": f"""{winrate_line}
            ```yaml\n    W: {wins}   |   L: {loses}```""", "inline": "false"},
            #{"name": f"Links", "value": f"{description}", "inline": "true"},
        ],
        "footer": {"text": f"Design by CMDRVo"},
    }

    embed = discord.Embed.from_dict(embed_dict)
    embed.timestamp = datetime.datetime.now()

    return embed

def last_game_page_1_embed(stats):
    #if stats['get']:
    #match data
    match_id = stats['id']
    match_map = stats['map']
    length = stats['time']
    score = stats['score'].replace('-', '/')
    date =  datetime.datetime.fromtimestamp(stats['started_at'], datetime.timezone.utc).astimezone().strftime("%m-%d-%Y")

    #main player data
    name = stats['players']['0']['name']
    avatar = stats['players']['0']['avatar']
    elo = stats['players']['0']['elo']
    lvl = stats['players']['0']['lvl']

    #stats
    kills = stats['players']['0']['kills']
    deaths = stats['players']['0']['deaths']
    assists = stats['players']['0']['assists']
    kr = stats['players']['0']['kr']
    hs = stats['players']['0']['hs']
    kd = stats['players']['0']['kd']

    #getting the rest
    lvl_emoji = config.lvls[int(lvl)]

    #length
    minutes = int(length // 60)
    seconds = int(length % 60)

    #score line
    t1_s, t2_s = score.split('/')
    green_line = config.green_line
    red_line = config.red_line

    greenSquare = int(t1_s)
    redSquare = int(t2_s)

    if greenSquare > redSquare:
        diff = round((greenSquare - redSquare)/1.33)
        greenSquare = 12
        redSquare = 12 - diff
    else:
        diff = round((redSquare - greenSquare)/1.33)
        redSquare = 12
        greenSquare = 12 - diff

    score_line = f"{''.replace('', green_line*greenSquare, 1)}\n{''.replace('', red_line*redSquare, 1)}"

    #result
    r = ''
    if int(stats['players']['0']['result']):
        r = 'Win'
    else:
        r = 'Lose'

    embed_dict = {
        "title": f"Last Match Stats - {match_map}",
        "description": f'''
        ᅟᅟᅟᅟᅟᅟᅟᅟ[Link](https://www.faceit.com/en/csgo/room/{match_id})               
        `              {date}              `''',
        "color": 0x4899FF,
        "timestamp": datetime.datetime.now().isoformat(),
        "author": {
            "name": f'{name}',
            "icon_url": f'{avatar}',
        },
        "thumbnail": {"url": f'{avatar}'},
        "fields": [
            #{"name": "Link", "value": f'[Match](https://www.faceit.com/en/csgo/room/{id})', "inline": "true"},
            {"name": f"Rating <{lvl_emoji}>", "value": f'```yaml\n{elo}```', "inline": "true"},
            {"name": "Lenght", "value": f'```yaml\n{minutes}m {seconds}s```', "inline": "true"},
            {"name": "Result", "value": f'```yaml\n{r}```', "inline": "true"},
            {"name": "KRR", "value": f'```yaml\n{kr}```', "inline": "true"},
            {"name": "KDR", "value": f'```yaml\n{kd}```', "inline": "true"},
            {"name": "HS ratio", "value": f'```yaml\n{hs}%```', "inline": "true"},
            {"name": "Kills", "value": f'```yaml\n{kills}```', "inline": "true"},
            {"name": "Deaths", "value": f'```yaml\n{deaths}```', "inline": "true"},
            {"name": "Assists", "value": f'```yaml\n{assists}```', "inline": "true"},
            {"name": "Score", "value": f"""{score_line}
            ```yaml\n             {score}```""", "inline": "false"},
        ],
        "footer": {"text": f"Design by CMDRVo"}
    }

    embed = discord.Embed.from_dict(embed_dict)
    embed.timestamp = datetime.datetime.now()

    return embed

def last_game_page_2_embed(stats):
    match_map = stats['map']
    score = stats['score'].replace('-', '/')
    date =  datetime.datetime.fromtimestamp(stats['started_at'], datetime.timezone.utc).astimezone().strftime("%d, %A, %B")

    #main player data
    name = stats['players']['0']['name']
    avatar = stats['players']['0']['avatar']
    embed_dict = {
        "title": f"Last Match Stats - {match_map} | {score}",
        "description": f'''```\n                Players of the game\n```''',
        "color": 0x4899FF,
        "timestamp": datetime.datetime.now().isoformat(),
        "author": {
            "name": f'{name}',
            "icon_url": f'{avatar}',
        },
        #"thumbnail": {"url": f'{faceit_avatar}'},
        # "fields": [
        #     #{"name": "Link", "value": f'[Match](https://www.faceit.com/en/csgo/room/{id})', "inline": "true"},
        #     {"name": f"{f1}", "value": f'''```yaml\nK / D / A / KR / KD\n{f1_k} / {f1_d} / {f1_a} / {f1_kr} / {f1_kd}```''', "inline": "true"},
        #     {"name": f"{s1}", "value": f'''```fix\nK / D / A / KR / KD\n{s1_k} / {s1_d} / {s1_a} / {s1_kr} / {s1_kd}```''', "inline": "true"},
        #     {"name": "\u200B", "value": f'\u200B', "inline": "true"},
        #     {"name": f"{f2}", "value": f'''```yaml\nK / D / A / KR / KD\n{f2_k} / {f2_d} / {f2_a} / {f2_kr} / {f2_kd}```''', "inline": "true"},
        #     {"name": f"{s2}", "value": f'''```fix\nK / D / A / KR / KD\n{s2_k} / {s2_d} / {s2_a} / {s2_kr} / {s2_kd}```''', "inline": "true"},
        #     {"name": "\u200B", "value": f'\u200B', "inline": "true"},
        #     {"name": f"{f3}", "value": f'''```yaml\nK / D / A / KR / KD\n{f3_k} / {f3_d} / {f3_a} / {f3_kr} / {f3_kd}```''', "inline": "true"},
        #     {"name": f"{s3}", "value": f'''```fix\nK / D / A / KR / KD\n{s3_k} / {s3_d} / {s3_a} / {s3_kr} / {s3_kd}```''', "inline": "true"},
        #     {"name": "\u200B", "value": f'\u200B', "inline": "true"},
        #     {"name": f"{f4}", "value": f'''```yaml\nK / D / A / KR / KD\n{f4_k} / {f4_d} / {f4_a} / {f4_kr} / {f4_kd}```''', "inline": "true"},
        #     {"name": f"{s4}", "value": f'''```fix\nK / D / A / KR / KD\n{s4_k} / {s4_d} / {s4_a} / {s4_kr} / {s4_kd}```''', "inline": "true"},
        #     {"name": "\u200B", "value": f'\u200B', "inline": "true"},
        #     {"name": f"{f5}", "value": f'''```yaml\nK / D / A / KR / KD\n{f5_k} / {f5_d} / {f5_a} / {f5_kr} / {f5_kd}```''', "inline": "true"},
        #     {"name": f"{s5}", "value": f'''```fix\nK / D / A / KR / KD\n{s5_k} / {s5_d} / {s5_a} / {s5_kr} / {s5_kd}```''', "inline": "true"},
        #     {"name": "\u200B", "value": f'\u200B', "inline": "true"},
        # ],
        "footer": {"text": f"Design by CMDRVo"},
    }

    embed = discord.Embed.from_dict(embed_dict)
    k = 0
    for i in ['0', '5', '1', '6', '2', '7', '3', '8', '4', '9']:
        player = stats["players"][f'{i}']
        f_name = f'{player["name"]}'
        
        if k % 2 == 0:
            colour = 'yaml'
        else:
            colour = 'fix'

        f_value = f'''```{colour}\nK / D / A / KR / KD\n{player['kills']} / {player['deaths']} / {player['assists']} / {player['kr']} / {player['kd']}```'''
        embed.add_field(name = f_name, value = f_value, inline = True)
        if k % 2 == 1:
            embed.add_field(name = '\u200B', value = '\u200B', inline = True)
        k +=1

    embed.timestamp = datetime.datetime.now()

    return embed

def lifetime_stats_embed(stats, description):
    #main data
    name = stats['name']
    avatar = stats['avatar']
    elo = stats['elo']
    lvl = stats['lvl']

    #stats
    kills = stats['kills']
    deaths = stats['deaths']
    t_kills = stats['kills_total']
    t_deaths = stats['deaths_total']
    kr = stats['kr']
    hs = stats['hs']
    kd = stats['kd']
    winrate = int(stats['winrate'])
    matches = stats['matches']
    wins = stats['wins']
    loses = stats['loses']
    streak = stats['streak']
    recent_results = stats['recent_results']

    #streak
    recent_streak = ''
    for i in recent_results:
        recent_streak += i

    recent_streak = recent_streak.replace('1','W').replace('0','L')

    #getting the rest
    lvl_emoji = config.lvls[int(lvl)]

    #winrate line
    green_line = config.green_line
    red_line = config.red_line

    greenSquare = round(winrate/8.33)
    redSquare = 12 - greenSquare
    winrate_line = ''.replace('', green_line*greenSquare, 1) + ''.replace('', red_line*redSquare, 1)

    embed_dict = {
        "title": f"Lifetime Competitive Stats",
        "description": f'{description}',
        "color": 0x4899FF,
        "timestamp": datetime.datetime.now().isoformat(),
        "author": {
            "name": f'{name}',
            "icon_url": f'{avatar}',
        },
        "thumbnail": {"url": f'{avatar}'},
        "fields": [
            {"name": "KRR", "value": f'```yaml\n{kr}```', "inline": "true"},
            {"name": "KDR", "value": f'```yaml\n{kd}```', "inline": "true"},
            {"name": f"Rating <{lvl_emoji}>", "value": f'```yaml\n{elo}```', "inline": "true"},
            {"name": "Avg Kills", "value": f'```yaml\n{kills}```', "inline": "true"},
            {"name": "Avg Deaths", "value": f'```yaml\n{deaths}```', "inline": "true"},
            {"name": "Avg HS", "value": f'```yaml\n{hs}%```', "inline": "true"},
            {"name": "Total Kills", "value": f'```yaml\n{t_kills}```', "inline": "true"},
            {"name": "Total Deaths", "value": f'```yaml\n{t_deaths}```', "inline": "true"},
            {"name": "Matches", "value": f'```yaml\n{matches}```', "inline": "true"},
            {"name": "Last 5 Games", "value": f'```yaml\n{recent_streak}```', "inline": "true"},
            {"name": "Longest Winstreak", "value": f'```yaml\n{streak}```', "inline": "true"},
            {"name": f"Winrate - {winrate}%", "value": f"""{winrate_line}
            ```yaml\n    W: {wins}   |   L: {loses}```""", "inline": "false"},
        ],
        "footer": {"text": f"Design by CMDRVo"},
    }

    embed = discord.Embed.from_dict(embed_dict)
    embed.timestamp = datetime.datetime.now()
    
    return embed
