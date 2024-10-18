from celery import Celery
from os import getenv
from dotenv import load_dotenv

load_dotenv()

def make_celery(app_name=__name__):
    redis_url = getenv('REDIS_URL', 'redis://localhost:6379/0')
    return Celery(app_name, broker=redis_url)

celery = make_celery()