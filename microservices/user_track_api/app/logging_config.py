import logging
from logging.config import dictConfig

def setup_logging():
    dictConfig({
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s [%(name)s.%(module)s]: %(message)s',
            }
        },
        'handlers': {
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
                'formatter': 'default'
            }
        },
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
    })

setup_logging()
logger = logging.getLogger("user_track_api")