import cassiopeia as cass
from cassiopeia.data import Queue, Continent
from cassiopeia.core import Account, ChampionMastery, MatchHistory, Summoner, CurrentMatch, Match
from merakicommons.container import SearchError

def is_in_game(summoner):
    try:
        current_match = CurrentMatch(summoner=summoner)
        if current_match.queue == Queue.ranked_solo_fives:
            return True
    except:
        return False
    return False

def get_last_10_matches(summoner : Summoner):
    # Get the last 10 matches of the summoner in solo queue
    match_history = MatchHistory(puuid=summoner.puuid, continent=Continent.europe, queue=Queue.ranked_solo_fives, count=10)
    last_10_matches = []
    match : Match
    for match in match_history:
        participant = match.participants[summoner]
        if match.duration.total_seconds() < 300:
            continue
        match_info = {
            'result': 'win' if participant.stats.win else 'lose',
            'champion_image': participant.champion.image.url
        }
        last_10_matches.append(match_info)
    last_10_matches.reverse()
    return last_10_matches

def get_all_summoners(summoners : dict):
    all_summoners_infos = []
    for name, summoner in summoners.items():
        account = Account(name=summoner.split('#')[0], tagline=summoner.split('#')[1], region='EUW')
        summoner = account.summoner
        summoner_infos = {}
        summoner_infos['name'] = name
        summoner_infos['pseudo'] = account.name_with_tagline
        summoner_infos['image'] = summoner.profile_icon().url

        entries = account.summoner.league_entries
        try:
            solo_ranked = entries.find(Queue.ranked_solo_fives)
            summoner_infos['tier'] = solo_ranked.tier.value
            summoner_infos['division'] = solo_ranked.division.value
            summoner_infos['lp'] = solo_ranked.league_points
            summoner_infos['games_played'] = solo_ranked.wins + solo_ranked.losses
            summoner_infos['win'] = solo_ranked.wins
            summoner_infos['lose'] = solo_ranked.losses
            summoner_infos['winrate'] = round(solo_ranked.wins / (solo_ranked.wins + solo_ranked.losses) * 100, 2)
            summoner_infos['most_played_champ'] = {}
            summoner_infos['last_matches'] = get_last_10_matches(summoner)
            summoner_infos['in_game'] = is_in_game(summoner)
        except SearchError:
            summoner_infos['tier'] = 'UNRANKED'
            summoner_infos['division'] = '0'
            summoner_infos['lp'] = 0
            summoner_infos['games_played'] = 0
            summoner_infos['win'] = 0
            summoner_infos['lose'] = 0
            summoner_infos['winrate'] = 0
            summoner_infos['most_played_champ'] = {}
            summoner_infos['last_matches'] = []
            summoner_infos['in_game'] = False
        if not summoner.champion_masteries[0]:
            break
        champ: ChampionMastery
        champ = summoner.champion_masteries[0]
        summoner_infos['most_played_champ'] = {}
        summoner_infos['most_played_champ']['name'] = champ.champion().name
        summoner_infos['most_played_champ']['image'] = champ.champion().image().url
        all_summoners_infos.append(summoner_infos)
    return all_summoners_infos