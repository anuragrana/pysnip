import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'large': {
            'format': '%(asctime)s  %(levelname)s  %(process)d  %(pathname)s  ' +
                      '%(funcName)s  %(lineno)d  %(message)s  '
        }
    },
    'handlers': {
        'errors_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight',
            'interval': 1,
            'filename': os.path.join(BASE_DIR, 'logs/errors.log'),
            'formatter': 'large',
        },
        'info_file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight',
            'interval': 1,
            'filename': os.path.join(BASE_DIR, 'logs/info.log'),
            'formatter': 'large',
        },
    },
    'loggers': {
        'error': {
            'handlers': ['errors_file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'info': {
            'handlers': ['info_file'],
            'level': 'INFO',
            'propagate': False,
        },

    },

}
