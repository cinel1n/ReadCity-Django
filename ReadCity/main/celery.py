import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ReadCity.settings')
app = Celery('main', broker_connection_retry=False,
             broker_connection_retry_on_startup=True, )
app.config_from_object('django.conf:settings')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'delete-old-viewed-books-every-day': {
        'task': 'main.tasks.clean_viewed',
        'schedule': crontab(minute=0, hour=0),
    },
}