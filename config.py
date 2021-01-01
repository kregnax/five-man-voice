import os

ENV = os.getenv('ENV').lower() if 'ENV' in os.environ else 'dev'
ADMIN_ID = int(os.getenv('DISCORD_ADMIN_ID'))
BOT_KEY = os.getenv('FIVE_MAN_DEV_KEY') if ENV == 'dev' else os.getenv(
    'FIVE_MAN_VOICE_KEY')
