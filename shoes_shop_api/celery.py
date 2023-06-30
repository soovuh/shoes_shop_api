import os
from celery import Celery
from celery.schedules import crontab

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shoes_shop_api.settings')

app = Celery('shoes_shop_api')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'clear_expired_carts': {
        'task': 'cart.tasks.clear_expired_carts',
        'schedule': crontab(minute='*/30')
    },
}
