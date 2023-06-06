import sys

from logger import log

TOKEN = ''

try:
    token_file = open('tgtoken')
    TOKEN = token_file.read()
    token_file.close()
except Exception as any_ex:
    log.e(exception=any_ex)
    sys.exit()

TELEGRAM_API_URL = f'https://api.telegram.org/bot{TOKEN}'
GET_UPDATES_URL = TELEGRAM_API_URL + '/getUpdates'
SEND_MESSAGE_URL = TELEGRAM_API_URL + '/sendMessage'
