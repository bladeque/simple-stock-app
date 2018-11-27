import os
import re

import requests
from celery import Celery
from django.apps import apps, AppConfig
from django.conf import settings
from django.core.cache import cache

if not settings.configured:
    # set the default Django settings module for the 'celery' program.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')  # pragma: no cover


app = Celery('backend')
# Using a string here means the worker will not have to
# pickle the object when using Windows.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')


class CeleryAppConfig(AppConfig):
    name = 'backend.taskapp'
    verbose_name = 'Celery Config'

    def ready(self):
        installed_apps = [app_config.name for app_config in apps.get_app_configs()]
        app.autodiscover_tasks(lambda: installed_apps, force=True)

        if hasattr(settings, 'RAVEN_CONFIG'):
            # Celery signal registration
# Since raven is required in production only,
            # imports might (most surely will) be wiped out
            # during PyCharm code clean up started
            # in other environments.
            # @formatter:off
            from raven import Client as RavenClient
            from raven.contrib.celery import register_signal as raven_register_signal
            from raven.contrib.celery import register_logger_signal as raven_register_logger_signal
# @formatter:on

            raven_client = RavenClient(dsn=settings.RAVEN_CONFIG['dsn'])
            raven_register_logger_signal(raven_client)
            raven_register_signal(raven_client)


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')  # pragma: no cover


@app.task()
def fetch_company_info(best_matches):
    for company in best_matches:
        name = company['2. name']
        symbol = company['1. symbol']

        resp = requests.get(
            settings.CLEARBIT_API_URL,
            # TODO: extend regex to strip other common terms
            params={'query': re.sub(r'\s(Inc?.|L.P.|Ltd?.)', '', name)},
        )

        try:
            top_match = resp.json() and resp.json()[0]
        except ValueError:
            # TODO: Log an error and continue
            continue

        domain = top_match and f'//{top_match["domain"]}'
        logo_url = top_match and top_match['logo']

        company_info = {
            'symbol': symbol,
            'name': name,
            'marketOpen': company['5. marketOpen'],
            'marketClose': company['6. marketClose'],
            'url': domain,
            'logo_url': logo_url,
        }

        cache.set(f'info_{symbol}', company_info)
