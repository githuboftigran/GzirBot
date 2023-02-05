__token = ''
try:
    __token_file = open('tgtoken')
    __token = __token_file.read()
    __token_file.close()
except:
    print('Could not read token file')

__url = 'https://api.telegram.org/bot{}'.format(__token)
get_updates_url = __url + '/getUpdates'
send_message_url = __url + '/sendMessage'
