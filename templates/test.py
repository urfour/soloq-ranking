import cassiopeia as cass
from dotenv import load_dotenv
from os import getenv

load_dotenv()
RIOT_API_KEY = getenv('RIOT_API_KEY')
cass.set_riot_api_key(RIOT_API_KEY)
print('Using Riot API key:', RIOT_API_KEY)

REAL_SUMMONERS = {
    'Bousilleur2Fion#SCUL': '',
    'Destructeur2vulv#SCUL': '',
    'chef dé kayoux#SCUL': '',
    'Malaxeur2Bzez#SCUL': '',
    'Pourfendeur2Fiak#SCUL': '',
    'Extincteur2Teuch#SCUL': '',
    'Enchaineur2Renoi#SCUL': '',
    'marteleurdetrous#SCUL': '',
    'EmpereurDesZebis#SCUL': '',
} 

if __name__ == '__main__':
    load_dotenv()
    RIOT_API_KEY = getenv('RIOT_API_KEY')
    cass.set_riot_api_key(RIOT_API_KEY)
    print('Using Riot API key:', RIOT_API_KEY)
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=update_summoners_info, trigger="interval", minutes=5)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())

    update_summoners_info()
    app.run(host='0.0.0.0', debug=True)