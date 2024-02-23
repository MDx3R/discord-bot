from concurrent.futures import ThreadPoolExecutor
from .faceit_api import *
import time

def process_match(player_id, elo, match_id, last_match, match_data):
    d = dict()

    d['match_id'] = match_id
    d['kills'] = 0
    d['deaths'] = 0
    d['assists'] = 0
    d['kr'] = 0.0
    d['hs'] = 0
    d['hs_p'] = 0
    d['kd'] = 0.0
    d['wins'] = 0
    d['results_change'] = []
    d['kr_change'] = []
    d['kd_change'] = []

    match_stats = faceit_get_match_stats(match_id)
    try:
        teams = match_stats['rounds'][0]['teams']
        d['rounds'] = int(match_stats['rounds'][0]['round_stats']['Rounds'])
        for p in range(2):
            players_list = teams[p]['players']
            for i in range(len(players_list)):
                if players_list[i]['player_id'] == player_id:
                    player_stats = players_list[i]['player_stats']
                    d['kills'] += int(player_stats['Kills'])
                    d['deaths'] += int(player_stats['Deaths'])
                    d['assists'] += int(player_stats['Assists'])
                    d['kr'] += float(player_stats['K/R Ratio'])
                    d['hs'] += int(player_stats['Headshots'])
                    d['hs_p'] += int(player_stats['Headshots %'])
                    d['kd'] += float(player_stats['K/D Ratio'])
                    d['wins'] += int(player_stats['Result'])
                    #добавить w/l для elo графика
                    #results +=[int(players_list[i]['player_stats']['Result'])]
                    d['results_change'] +=[int(player_stats['Result'])]
                    d['kr_change'] += [float(player_stats['K/R Ratio'])]
                    d['kd_change'] += [float(player_stats['K/D Ratio'])]

        if match_id == last_match:
            stats = dict()
            match_stats = match_stats['rounds'][0]

            rounds = int(match_stats['round_stats']['Rounds'])

            stats['id'] = match_stats['match_id']
            stats['rounds'] = rounds
            stats['map'] = match_stats['round_stats']['Map']
            stats['started_at'] = match_data['started_at']
            stats['finished_at'] = match_data['finished_at']
            stats['time'] = match_data['finished_at'] - match_data['started_at']
            stats['players'] = dict()

            #match analysis
            teams = match_stats['teams']

            pi_team = 0
            si_team = 0

            p_team = []
            s_team = []

            #searching for a player
            for i in range(2):
                team = teams[i]['players']
                for j in range(len(team)):
                    if team[j]['player_id'] == player_id:
                        pi_team = i
                        si_team = 1-i
                        break
                if pi_team != si_team:
                    break
            
            #processing first team
            team = teams[pi_team]['players']
            for i in range(len(team)):
                p_team.append(team[i]['player_id'])
            
            #sorting (requested player to the top)
            f_p = p_team[0]
            r_p = p_team.index(player_id)
            p_team[0] = player_id
            p_team[r_p] = f_p

            #creating a dict
            p_stats = dict()
            for i in range(len(p_team)):
                p_stats[p_team[i]] = dict()

            #filling the dict
            for i in range(len(team)):
                player = team[i]
                ind = player['player_id']
                p_stats[ind]['name'] = player['nickname']
                p_stats[ind]['id'] = player['player_id']
                p_stats[ind]['result'] = player['player_stats']['Result']
                p_stats[ind]['kills'] = player['player_stats']['Kills']
                p_stats[ind]['deaths'] = player['player_stats']['Deaths']
                p_stats[ind]['assists'] = player['player_stats']['Assists']
                p_stats[ind]['kr'] = player['player_stats']['K/R Ratio']
                p_stats[ind]['kd'] = player['player_stats']['K/D Ratio']
                p_stats[ind]['hs'] = player['player_stats']['Headshots']
                p_stats[ind]['hs%'] = player['player_stats']['Headshots %']

            #adding the player elo
            p_stats[player_id]['elo'] = elo

            #result of the game
            p_score = int(teams[pi_team]['team_stats']['Final Score'])
            p_is_win = int(teams[pi_team]['team_stats']['Team Win'])
            
            #processing second team
            team = teams[si_team]['players']
            for i in range(len(team)):
                s_team.append(team[i]['player_id'])

            #creating a dict
            s_stats = dict()
            for i in range(len(s_team)):
                s_stats[s_team[i]] = dict()

            #filling the dict
            for i in range(len(team)):
                player = team[i]
                ind = player['player_id']
                s_stats[ind]['name'] = player['nickname']
                s_stats[ind]['id'] = player['player_id']
                s_stats[ind]['result'] = player['player_stats']['Result']
                s_stats[ind]['kills'] = player['player_stats']['Kills']
                s_stats[ind]['deaths'] = player['player_stats']['Deaths']
                s_stats[ind]['assists'] = player['player_stats']['Assists']
                s_stats[ind]['kr'] = player['player_stats']['K/R Ratio']
                s_stats[ind]['kd'] = player['player_stats']['K/D Ratio']
                s_stats[ind]['hs'] = player['player_stats']['Headshots']
                s_stats[ind]['hs%'] = player['player_stats']['Headshots %']

            #memorizing name of the team
            #can be deleted if decided to check every player's data to retrieve elo, lvl and avatar
            teams = match_data['teams']
            pi2_team = 0
            si2_team = 0

            for i in teams:
                #team = teams[i]['roster']
                team = teams[i]['players']
                for j in range(len(team)):
                    if team[j]['player_id'] == player_id:
                        pi2_team = i
                        if i == 'faction1':
                            si2_team = 'faction2'
                        else:
                            si2_team = 'faction1'
                        break
                if pi2_team != si2_team:
                    break

            #adding avatars and lvls
            for i in teams:
                #team = teams[i]['roster']
                team = teams[i]['players']
                for j in range(len(team)):
                    if pi2_team == i:
                        p_stats[team[j]['player_id']]['avatar'] = team[j]['avatar']
                        p_stats[team[j]['player_id']]['lvl'] = team[j]['skill_level']
                    else:
                        #print(team[j]['player_id'])
                        s_stats[team[j]['player_id']]['avatar'] = team[j]['avatar']
                        s_stats[team[j]['player_id']]['lvl'] = team[j]['skill_level']

            #uniting two dicts into one
            b_team = p_team + s_team
            for i in range(len(b_team)):
                pl_id = b_team[i]
                if pl_id in p_team:
                    stats['players'][f'{i}'] = p_stats[pl_id]
                else:
                    stats['players'][f'{i}'] = s_stats[pl_id]

            #checking the result of the game
            if p_is_win:
                score = f'{p_score}-{rounds-p_score}'
                stats['winner_score'] = p_score
            else:
                score = f'{rounds-p_score}-{p_score}'
                stats['winner_score'] = rounds-p_score

            stats['score'] = score

            d['last'] = stats

        d['status'] = True
        return d
    
    except ValueError:
        d['status'] = False

        return d

def process_recent_games(l):
    nickname, player_id, data, matches_list, matches_data = l
    stats = dict()
    s = stats['stats'] = dict()

    stats['name'] = nickname
    stats['id'] = player_id

    try:
    #if True:
        elo = data['games']['csgo']['faceit_elo']

        #main data
        stats['steam_id'] = data['steam_id_64']
        stats['elo'] = elo
        stats['lvl'] = data['games']['csgo']['skill_level']
        stats['avatar'] =  data['avatar']
        stats['wall'] =  data['cover_image']

        stats['games'] = len(matches_list)

        stats['last_game'] = matches_list[0]
        stats['matches_list'] = matches_list

        with ThreadPoolExecutor(len(matches_list)) as executor:
            p_stats = executor.map(process_match, [player_id]*len(matches_list), [elo]*len(matches_list), matches_list, [matches_list[0]]*len(matches_list), matches_data)
            p_stats = [i for i in p_stats]

        #main stats
        g_keys = ['results_change', 'kr_change', 'kd_change']
        m_keys = ["kills", "deaths", "assists", "hs", "rounds", "wins"]
        keys = m_keys+g_keys
        for i in keys:
            if i in m_keys:
                s[i] = 0
            else:
                stats[i] = []
        for i in range(len(p_stats)):
            match_stats = p_stats[i]
            if match_stats['status'] or 'match_id' in match_stats:
                for j in keys:
                    if j in m_keys:
                        s[j] += match_stats[j]
                    else:
                        stats[j] += match_stats[j]

        #main stats calculations
        s['t_kills'] = s['kills']
        s['t_deaths'] = s['deaths']
        s['t_assists'] = s['assists']
        s['kr'] = round(s['kills']/s['rounds'], 2)
        s['kd'] = round(s['kills']/s['deaths'], 2)
        s['hs%'] = round(s['hs']*(100/s['kills']))
        s['winrate'] = round(s['wins']*(100/len(matches_list)))
        s['loses'] = len(matches_list) - s['wins']
        s['kills'] = round(s['kills']/len(matches_list), 2)
        s['deaths'] = round(s['deaths']/len(matches_list), 2)
        s['assists'] = round(s['assists']/len(matches_list), 2)

        t_elo = [elo]
        for i in stats['results_change']:
            t_elo += [t_elo[len(t_elo)-1]-25 if i == 1 else t_elo[len(t_elo)-1]+25]

        stats['elo_change'] = t_elo[:-1]

        stats['matches_stats'] = p_stats
        stats['status'] = True

        #print(stats)
        return stats
    
    except KeyError:
        stats['status'] = False

        return stats


def process_lastgame(l):
    nickname, player_id, data, match_id = l
    stats = dict()
    elo = data['games']['csgo']['faceit_elo']
    try:
        match_data = faceit_get_match_stats(match_id)
        match_data = match_data['rounds'][0]

        rounds = int(match_data['round_stats']['Rounds'])

        stats['id'] = match_data['match_id']
        stats['rounds'] = rounds
        stats['map'] = match_data['round_stats']['Map']
        stats['started_at'] = data['started_at']
        stats['finished_at'] = data['finished_at']
        stats['time'] = data['finished_at'] - data['started_at']
        stats['players'] = dict()

        #match analysis
        teams = match_data['teams']

        pi_team = 0
        si_team = 0

        p_team = []
        s_team = []

        #searching for a player
        for i in range(2):
            team = teams[i]['players']
            for j in range(len(team)):
                if team[j]['player_id'] == player_id:
                    pi_team = i
                    si_team = 1-i
                    break
            if pi_team != si_team:
                break
        
        #processing first team
        team = teams[pi_team]['players']
        for i in range(len(team)):
            p_team.append(team[i]['player_id'])
        
        #sorting (requested player to the top)
        f_p = p_team[0]
        r_p = p_team.index(player_id)
        p_team[0] = player_id
        p_team[r_p] = f_p

        #creating a dict
        p_stats = dict()
        for i in range(len(p_team)):
            p_stats[p_team[i]] = dict()

        #filling the dict
        for i in range(len(team)):
            player = team[i]
            ind = player['player_id']
            p_stats[ind]['name'] = player['nickname']
            p_stats[ind]['id'] = player['player_id']
            p_stats[ind]['result'] = player['player_stats']['Result']
            p_stats[ind]['kills'] = player['player_stats']['Kills']
            p_stats[ind]['deaths'] = player['player_stats']['Deaths']
            p_stats[ind]['assists'] = player['player_stats']['Assists']
            p_stats[ind]['kr'] = player['player_stats']['K/R Ratio']
            p_stats[ind]['kd'] = player['player_stats']['K/D Ratio']
            p_stats[ind]['hs'] = player['player_stats']['Headshots']
            p_stats[ind]['hs%'] = player['player_stats']['Headshots %']

        #adding the player elo
        p_stats[player_id]['elo'] = elo

        #result of the game
        p_score = int(teams[pi_team]['team_stats']['Final Score'])
        p_is_win = int(teams[pi_team]['team_stats']['Team Win'])
        
        #processing second team
        team = teams[si_team]['players']
        for i in range(len(team)):
            s_team.append(team[i]['player_id'])

        #creating a dict
        s_stats = dict()
        for i in range(len(s_team)):
            s_stats[s_team[i]] = dict()

        #filling the dict
        for i in range(len(team)):
            player = team[i]
            ind = player['player_id']
            s_stats[ind]['name'] = player['nickname']
            s_stats[ind]['id'] = player['player_id']
            s_stats[ind]['result'] = player['player_stats']['Result']
            s_stats[ind]['kills'] = player['player_stats']['Kills']
            s_stats[ind]['deaths'] = player['player_stats']['Deaths']
            s_stats[ind]['assists'] = player['player_stats']['Assists']
            s_stats[ind]['kr'] = player['player_stats']['K/R Ratio']
            s_stats[ind]['kd'] = player['player_stats']['K/D Ratio']
            s_stats[ind]['hs'] = player['player_stats']['Headshots']
            s_stats[ind]['hs%'] = player['player_stats']['Headshots %']

        #memorizing name of the team
        #can be deleted if i decide to check every player's data to retrieve elo, lvl and avatar
        teams = data['teams']
        pi2_team = 0
        si2_team = 0

        for i in teams:
            team = teams[i]['roster']
            for j in range(len(team)):
                if team[j]['player_id'] == player_id:
                    pi2_team = i
                    if i == 'faction1':
                        si2_team = 'faction2'
                    else:
                        si2_team = 'faction1'
                    break
            if pi2_team != si2_team:
                break

        #adding avatars and lvls
        for i in teams:
            team = teams[i]['roster']
            for j in range(len(team)):
                if pi2_team == i:
                    p_stats[team[j]['player_id']]['avatar'] = team[j]['avatar']
                    p_stats[team[j]['player_id']]['lvl'] = team[j]['game_skill_level']
                else:
                    #print(team[j]['player_id'])
                    s_stats[team[j]['player_id']]['avatar'] = team[j]['avatar']
                    s_stats[team[j]['player_id']]['lvl'] = team[j]['game_skill_level']

        #uniting two dicts into one
        b_team = p_team + s_team
        for i in range(len(b_team)):
            pl_id = b_team[i]
            if pl_id in p_team:
                stats['players'][f'{i}'] = p_stats[pl_id]
            else:
                stats['players'][f'{i}'] = s_stats[pl_id]

        #checking the result of the game
        if p_is_win:
            score = f'{p_score}-{rounds-p_score}'
            stats['winner_score'] = p_score
        else:
            score = f'{rounds-p_score}-{p_score}'
            stats['winner_score'] = rounds-p_score

        stats['score'] = score
        stats['get'] = True

        return (1, stats)
    
    except KeyError:
        stats['id'] = match_id
        keys = ["rounds", "map", "started_at", "finished_at", "time", "winner_score"]
        for i in keys:
            stats[i] = 0
        stats['score'] = '0-0'
        s = stats['players'] = dict()
        m_keys = ['kills', 'deaths', 'assists', 'kr', 'kd', 'hs', 'hs%', 'result', 'elo', 'lvl']
        n_keys = ['name', 'id']
        keys = n_keys + m_keys
        for i in range(0, 10):
            s[f'{i}'] = dict()
        for i in range(0, 10):
            for j in keys:
                if j in m_keys:
                    s[f'{i}'][j] = 0
                else:
                    s[f'{i}'][j] = 'None'
                    
        s['0']['name'] = nickname
        s['0']['id'] = player_id
        s['0']['avatar'] = ''

        stats['get'] = False

        return (0, stats)

def process_lifetime(l):
    nickname, player_id, data, l_stats = l
    stats = dict()

    stats['name'] = nickname
    stats['id'] = player_id

    try:
        #start filling
        level = str(data['games']['csgo']['skill_level'])
        elo = data['games']['csgo']['faceit_elo']

        #add avatar and wall
        stats['elo'] = elo
        stats['lvl'] = level
        stats['avatar'] =  data['avatar']
        stats['wall'] = data['cover_image']

        kills = 0
        deaths = 0
        assists = 0
        rounds = 0.0
        matches = 0
        wins = 0
        hs = 0

        map_list = ["de_ancient", "de_cache", "de_dust2", "de_overpass", "de_inferno", "de_train", "de_nuke", "de_cbble", "de_mirage", "de_vertigo", "de_anubis"]

        #going throuth all maps ever played
        segments = l_stats['segments']
        for m in range(len(segments)):
            if segments[m]['label'] in map_list and (segments[m]['mode'] == "5v5" or segments[m]['mode'] == "5v5PREMADE"):
                r_s = segments[m]["stats"]
                kills += int(r_s['Kills'])
                deaths += int(r_s['Deaths'])
                rounds += int(r_s['Rounds'])
                matches += int(r_s['Matches'])
                wins += int(r_s['Wins'])
                hs += int(r_s['Headshots'])

        #filling the dict
        stats['matches'] = matches
        stats['wins'] = wins
        stats['loses'] = matches - wins
        stats['kills_total'] = kills
        stats['deaths_total'] = deaths
        stats['assists_total'] = assists
        stats['kills'] = round((kills/matches),2)
        stats['deaths'] = round((deaths/matches),2)
        stats['assists'] = round((assists/matches),2)
        stats['kr'] = round((kills/rounds),2)
        stats['kd'] = round((kills/deaths),2)
        stats['winrate'] = str(round(wins*(100/matches)))
        stats['hs'] = round(hs*(100/kills))
        
        stats['streak'] = l_stats['lifetime']['Longest Win Streak']
        stats['recent_results'] = l_stats['lifetime']['Recent Results']

        stats['status'] = True

        return stats
    
    except KeyError:
        stats['status'] = False
        
        return stats

funcs = [
    faceit_get_player_data, 
    faceit_get_matches, 
    faceit_get_match_details,
    faceit_get_match_stats,
    faceit_get_lifetime_stats,
    process_recent_games,
    process_lastgame,
    process_lifetime,
]   
def functions(n, l):
    if n == 1:
        return funcs[n](l)['items']
    return funcs[n](l)

def get_stats(nickname, player_id):
    stats = dict()

    with ThreadPoolExecutor(3) as executor:
        results = executor.map(functions, [0, 1, 4], [nickname, player_id, player_id])
        data, matches_data, lifetime = [i for i in results]
    
    matches_list = [matches_data[i]['match_id'] for i in range(len(matches_data))]
    if len(matches_list) > 0:

        full = [nickname, player_id, data, matches_list, matches_data]
        life = [nickname, player_id, data, lifetime]

        with ThreadPoolExecutor(3) as executor:
            results = executor.map(functions, [5, 7], [full, life])
            full, lifetime = [i for i in results]

        stats['recent'] = full
        if full['matches_stats'][0]['status']:
            stats['last'] = full['matches_stats'][0]['last']
            stats['last']['status'] = full['matches_stats'][0]['status']
        else:
            stats['last'] = dict()
            stats['last']['status'] = False
        stats['lifetime'] = lifetime

        return stats
    else:
        return 0