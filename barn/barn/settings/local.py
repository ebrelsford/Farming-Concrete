from .base import *


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'log_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PROJECT_ROOT, 'logs', 'django.log'),
            'maxBytes': '16777216', # 16megabytes
            'formatter': 'verbose'
        },
    },
    'root': {
        'handlers': ['log_file',],
        'level': 'DEBUG',
    },
}
