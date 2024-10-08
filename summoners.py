from opgg.opgg import OPGG
from opgg.summoner import Summoner, Game 
from opgg.league_stats import LeagueStats
import pandas as pd
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

        summoner_infos['recent_games'] = []
        for game in summoner.recent_game_stats[:3]:
            for champ in opgg.all_champions:
                if champ.id == game.myData.champion_id:
                    champion = champ.name
                    break
            game_info = {
                'champion': champion,
                'result': 'Victoire' if game.myData.stats.result == 'WIN' else 'Défaite',
                'kills': game.myData.stats.kill,
                'deaths': game.myData.stats.death,
                'assists': game.myData.stats.assist,
                'date': datetime.strptime(game.created_at, '%Y-%m-%dT%H:%M:%S%z')
            }
            summoner_infos['recent_games'].append(game_info)
        all_summoners_infos.append(summoner_infos)
    return all_summoners_infos
        
if __name__ == "__main__":
    df = pd.DataFrame(get_all_summoners())
    df.to_csv('summoners_infos.csv', index=False)