from celery.schedules import crontab
CELERY_BROKER_URL = "redis://redis:6379"
CELERY_RESULT_BACKEND = "redis://redis:6379"
CELERY_TIMEZONE = "Europe/Kiev"

CELERY_BEAT_SCHEDULE = {
    "scrapping_every_day": {
        "task": "tasks.scrapping_task",
        "schedule": crontab(minute=0, hour=0),
    },
    "dump_every_day": {
        "task": "tasks.dump_task",
        "schedule": crontab(minute=0, hour=0),
    },
}