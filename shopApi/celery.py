import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopApi.settings')

app = Celery('shopApi')  #name of project
app.config_from_object('django.conf:settings', namespace='CELERY') #the beggining of settings word to find in
app.autodiscover_tasks()

