from celery.schedules import crontab

beat_schedule = {
    'seed-videos-in-db': {
        'task': 'app.tasks.update_db_with_videos',
        # 'schedule': crontab(second='*/10'),
        'schedule': 10.0,    # for testing cron
        'kwargs': {'search_string': 'cricket'}
    },
}

