token = ''

try:
    token_file = open('tgtoken')
    token = token_file.read()
    token_file.close()
except:
    print('Could not read token file')

TELEGRAM_API_URL = f'https://api.telegram.org/bot{token}'
GET_UPDATES_URL = TELEGRAM_API_URL + '/getUpdates'
SEND_MESSAGE_URL = TELEGRAM_API_URL + '/sendMessage'
