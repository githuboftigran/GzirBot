token = ''

try:
    token_file = open('tgtoken')
    token = token_file.read()
    token_file.close()
except:
    print('Could not read token file')

telegram_api_url = f'https://api.telegram.org/bot{token}'
get_updates_url = telegram_api_url + '/getUpdates'
send_message_url = telegram_api_url + '/sendMessage'
