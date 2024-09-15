CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'

from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'rebalance-portfolios': {
        'task': 'portfolio.tasks.rebalance_portfolios',
        'schedule': crontab(minute='0', hour='*/1'),
    },
}
