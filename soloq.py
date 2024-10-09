from flask import Flask, render_template
from cachetools import TTLCache
from summoners import get_all_summoners
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import time

app = Flask(__name__)
cache = TTLCache(maxsize=100, ttl=600)
infos = []

REAL_SUMMONERS = {
    'Tom': 'Et Zééé Bardi#EUW',
    'Nassime': 'UrFour#suuuu',
    'Alex': 'Kahlazar#EUW',
    'Antoine': 'Big C le Cuisto#2715',
    'Pipo': 'Pipo le cuisto#EUW',
    'Guilhem': 'Bousilleur2Fion#SCUL',
    'Yann': 'Call me mummy#2811',
    'Zebi 2': 'EmpereurDesZebis#SCUL'
}

def rank_to_value(tier, division, lp):
    tiers = ['UNRANKED', 'IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND', 'MASTER', 'GRANDMASTER', 'CHALLENGER']
    divisions = ['IV', 'III', 'II', 'I', '0']
    tier_value = tiers.index(tier) * 4
    division_value = divisions.index(division)
    return tier_value + division_value + lp / 100

def update_summoners_info():
    global infos
    if 'summoners_infos' in cache:
        return
    else:
        cache['summoners_infos'] = get_all_summoners(REAL_SUMMONERS)
    infos.sort(key=lambda x: rank_to_value(x['tier'], x['division'], x['lp']), reverse=True)
    print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] Updated summoners info')

@app.route('/')
def index():
    return render_template('index.html', infos=cache['summoners_infos'])

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=update_summoners_info, trigger="interval", minutes=20)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())

    update_summoners_info()
    app.run(host='0.0.0.0')