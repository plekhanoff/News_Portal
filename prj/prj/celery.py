import os
from celery.schedules import crontab
from celery import Celery
import views


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prj.settings')

app = Celery('prj')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
'action_every_monday_8am': {
'task': 'prj.tasks.message_to_subscribers',
'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
'args': [views],
},
}





