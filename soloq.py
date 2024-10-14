from flask import Flask, render_template, jsonify
from os import getenv 
from dotenv import load_dotenv
from cachetools import TTLCache
import cassiopeia as cass
from summoners import get_all_summoners
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import time
from datetime import datetime, timedelta
import timeago

app = Flask(__name__)

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

updated_at = ''
summoners_infos = []

def rank_to_value(tier, division, lp):
    tiers = ['UNRANKED', 'IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND', 'MASTER', 'GRANDMASTER', 'CHALLENGER']
    divisions = ['IV', 'III', 'II', 'I', '0']
    tier_value = tiers.index(tier) * 4
    division_value = divisions.index(division)
    return tier_value + division_value + lp / 100

def update_summoners_info():
    global summoners_infos, updated_at
    summoners_infos = get_all_summoners(REAL_SUMMONERS)
    summoners_infos.sort(key=lambda x: rank_to_value(x['tier'], x['division'], x['lp']), reverse=True)
    updated_at = time.strftime("%d/%m/%Y %H:%M:%S")
    print(f'[{time.strftime("%d/%m/%Y %H:%M:%S")}] Updated summoners info')

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
                    "LeagueSummonerEntries": timedelta(minutes=5),
                }
            }, 
            'DDragon': {}, 
            'RiotAPI': {
                'api_key': RIOT_API_KEY
            }
        },
    })
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=update_summoners_info, trigger="interval", minutes=5)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())

    update_summoners_info()
    app.run(host='0.0.0.0')