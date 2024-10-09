from opgg.opgg import OPGG
from opgg.summoner import Summoner, Game
from opgg.league_stats import LeagueStats
from datetime import datetime

CHAMPIONS_ID = {}

def reconstruct_champions_id():
    global CHAMPIONS_ID
    if CHAMPIONS_ID:
        return
    opgg = OPGG()
    champions = opgg.all_champions
    champions_id = {}
    for champ in champions:
        champions_id[champ.name] = champ.id
    CHAMPIONS_ID = champions_id

def int_to_roman(input):
    int_roman = {
        0: '0',
        1: 'I',
        2: 'II',
        3: 'III',
        4: 'IV'
    }
    return int_roman[input]

def get_all_summoners(summoners : dict):
    opgg = OPGG()
    stat: LeagueStats
    all_summoners_infos = []
    summoner: Summoner
    game: Game
    reconstruct_champions_id
    for name, summoner in summoners.items():
        summoner = opgg.search(summoner, region='EUW')
        summoner_infos = {}
        summoner_infos['name'] = name
        summoner_infos['pseudo'] = f'{summoner.game_name}#{summoner.tagline.upper()}'
        summoner_infos['image'] = summoner.profile_image_url
        for stat in summoner.league_stats:
            if stat.queue_info.game_type == 'SOLORANKED':
                summoner_infos['tier'] = stat.tier_info.tier
                summoner_infos['division'] = int_to_roman(stat.tier_info.division)
                summoner_infos['lp'] = stat.tier_info.lp
                summoner_infos['games_played'] = stat.win + stat.lose
                summoner_infos['win'] = stat.win
                summoner_infos['lose'] = stat.lose
                summoner_infos['winrate'] = stat.win_rate
                if stat.updated_at:
                    summoner_infos['updated_at'] = datetime.strptime(stat.updated_at, '%Y-%m-%dT%H:%M:%S%z')
                else:
                    summoner_infos['updated_at'] = datetime.now()
                summoner_infos['most_played_champ'] = {}
                if not summoner.most_champions:
                    break
                champ = summoner.most_champions[0]
                summoner_infos['most_played_champ']['name'] = champ.champion.name
                summoner_infos['most_played_champ']['image'] = champ.champion.image_url
                summoner_infos['most_played_champ']['winrate'] = champ.win_rate
                summoner_infos['most_played_champ']['games_played'] = champ.play
                break
        all_summoners_infos.append(summoner_infos)
    return all_summoners_infos