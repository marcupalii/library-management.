
BROKER_HEARTBEAT = 0
CELERY_IMPORTS = ('app.tasks.routine')
CELERY_TASK_RESULT_EXPIRES = 30
CELERY_TIMEZONE = 'Europe/Bucharest'
ENABLE_UTC = True
CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# DATABASE_TABLE_NAMES ={
#     'task': 'schedule_log',
#     'group': 'schedule_log_group',
# }

CELERYBEAT_SCHEDULE = {
    'test-celery': {
        'task': 'app.tasks.routine.stable_matching_routine',
        'schedule': 90.0
    }
}
