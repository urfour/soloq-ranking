from flask import Flask, render_template
from os import getenv 
from dotenv import load_dotenv
from cachetools import TTLCache
import cassiopeia as cass
from summoners import get_all_summoners
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import time

app = Flask(__name__)
cache = TTLCache(maxsize=100, ttl=600)

REAL_SUMMONERS = {
    'Guilhem': 'Bousilleur2Fion#SCUL',
    'Pipo': 'Destructeur2vulv#SCUL',
    'Yann': 'chef dé kayoux#SCUL',
    'Antoine': 'Malaxeur2Bzez#SCUL',
    'Kahlabzez': 'Pourfendeur2Fiak#SCUL',
    'Nassime': 'Extincteur2Teuch#SCUL',
    'Loan': 'Enchaineur2Renoi#SCUL',
    'Zebi 2': 'EmpereurDesZebis#SCUL'
}

def rank_to_value(tier, division, lp):
    tiers = ['UNRANKED', 'IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND', 'MASTER', 'GRANDMASTER', 'CHALLENGER']
    divisions = ['IV', 'III', 'II', 'I', '0']
    tier_value = tiers.index(tier) * 4
    division_value = divisions.index(division)
    return tier_value + division_value + lp / 100

def update_summoners_info():
    if 'summoners_infos' in cache:
        return
    else:
        cache['summoners_infos'] = get_all_summoners(REAL_SUMMONERS)
        cache['summoners_infos'].sort(key=lambda x: rank_to_value(x['tier'], x['division'], x['lp']), reverse=True)
    print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] Updated summoners info')

@app.route('/')
def index():
    return render_template('index.html', infos=cache['summoners_infos'])

if __name__ == '__main__':
    load_dotenv()
    RIOT_API_KEY = getenv('RIOT_API_KEY')
    cass.set_riot_api_key(RIOT_API_KEY)
    print('Using Riot API key:', RIOT_API_KEY)
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=update_summoners_info, trigger="interval", minutes=20)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())

    update_summoners_info()
    app.run(host='0.0.0.0')