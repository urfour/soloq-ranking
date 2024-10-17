import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
from os import getenv 
from dotenv import load_dotenv
import cassiopeia as cass
from summoners import get_all_summoners
import time
from datetime import datetime, timedelta
import timeago

app = Flask(__name__)
socketio = SocketIO(app)

REAL_SUMMONERS = {
    'Guilhem': 'Bousilleur2Fion#SCUL',
    'Pipo': 'Destructeur2vulv#SCUL',
    'Yann': 'chef dé kayoux#SCUL',
    'Antoine': 'Malaxeur2Bzez#SCUL',
    'Kahlabzez': 'Pourfendeur2Fiak#SCUL',
    'Nassime': 'Extincteur2Teuch#SCUL',
    'Loan': 'Enchaineur2Renoi#SCUL',
    'Cuillères': 'marteleurdetrous#SCUL',
    'Dreamer': 'EmpereurDesZebis#SCUL'
}

updated_at = time.strftime("%d/%m/%Y %H:%M:%S")
summoners_infos = []
online_statuses = {}
old_online_statuses = {}

def rank_to_value(tier, division, lp):
    tiers = ['UNRANKED', 'IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND', 'MASTER', 'GRANDMASTER', 'CHALLENGER']
    divisions = ['IV', 'III', 'II', 'I', '0']
    tier_value = tiers.index(tier) * 4
    division_value = divisions.index(division)
    return tier_value + division_value + lp / 100

def background_task():
    while True:
        socketio.sleep(120)
        update_summoners_info()

def update_summoners_info():
    global old_online_statuses, online_statuses, summoners_infos, updated_at
    summoners_infos = get_all_summoners(REAL_SUMMONERS)
    summoners_infos.sort(key=lambda x: rank_to_value(x['tier'], x['division'], x['lp']), reverse=True)

    online_statuses = {summoner['name']: {'is_connected': summoner['is_connected'], 'current_game': summoner['current_game']} for summoner in summoners_infos}

    for name in REAL_SUMMONERS.keys():
        if name in old_online_statuses and name in online_statuses:
            current_status = online_statuses[name]['is_connected']
            current_game = online_statuses[name]['current_game']
            previous_status = old_online_statuses[name]['is_connected']
            if current_status and not previous_status:
                print(f'{name} is connected')
                socketio.emit('player_online', {'name': name, 'current_game': current_game})
            elif not current_status and previous_status:
                print(f'{name} is disconnected')
                socketio.emit('player_offline', {'name': name})
            else:
                socketio.emit('update_player_status', {'name': name, 'in_game': current_status})

    old_online_statuses = online_statuses.copy()

    updated_at = time.strftime("%d/%m/%Y %H:%M:%S")
    print(f'[{updated_at}] Updated summoners info')

@app.route('/')
def index():
    current_time = datetime.now()
    last_updated_time = datetime.strptime(updated_at, "%d/%m/%Y %H:%M:%S")
    time_difference = timeago.format(last_updated_time, current_time, 'fr')
    return render_template('index.html', infos=summoners_infos, updated_at=time_difference)

@app.route('/refresh', methods=['POST'])
def refresh():
    update_summoners_info()
    return jsonify({'status': 'success', 'updated_at': updated_at})

if __name__ == '__main__':
    load_dotenv()
    RIOT_API_KEY = getenv('RIOT_API_KEY')
    cass.apply_settings({
        'pipeline': {
            "Cache": {
                "expirations": {
                    "LeagueSummonerEntries": timedelta(minutes=3),
                    'Match': timedelta(minutes=3),
                    'CurrentMatch': timedelta(seconds=30),
                }
            }, 
            'DDragon': {}, 
            'RiotAPI': {
                'api_key': RIOT_API_KEY
            }
        },
    })
    socketio.start_background_task(background_task)
    update_summoners_info()
    if app.config['ENV'] == 'development':
        socketio.run(app, host='0.0.0.0')