import os

ENV = os.getenv('ENV').lower() if 'ENV' in os.environ else 'dev'

BOT_KEY = os.getenv('FIVE_MAN_DEV_KEY') if ENV == 'dev' else os.getenv(
    'FIVE_MAN_VOICE_KEY')
