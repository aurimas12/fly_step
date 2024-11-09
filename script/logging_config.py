from constants import logs_file_path

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s -  %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M',
        },
    },
    'handlers': {
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': logs_file_path,
             'mode': 'a',
            'encoding': 'utf-8',
            "maxBytes": 500000,
            "backupCount": 3,
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True
        },
    }
}
