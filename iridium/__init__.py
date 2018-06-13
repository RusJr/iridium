import logging.config

from iridium.browser import ChromeBrowser


# LOGGING TODO: hmm ----------------------------------------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {'ir_format': {'format': '[%(levelname)s] [%(asctime)s] [%(name)s:%(module)s:%(lineno)d] %(message)s',
                                 'datefmt': '%d/%m/%Y %H:%M:%S'}},
    'handlers': {
        'ir_handler': {'level': 'DEBUG', 'class': 'logging.StreamHandler', 'formatter': 'ir_format'},
    },
    'loggers': {
        'Iridium': {'handlers': ['ir_handler'], 'propagate': False, 'level': 'DEBUG'},
    }
}
logging.config.dictConfig(LOGGING)
