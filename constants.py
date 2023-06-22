import re

UPDATES_POLLING_TIMEOUT = 60
UPDATES_FAILURE_TIMEOUT = 60

UPDATE_INTERRUPTIONS_INTERVAL = 5 * 60

DAY_SECONDS = 60 * 60 * 24
INTERRUPTION_LIFESPAN = DAY_SECONDS

WHITESPACES_PATTERN = re.compile(r'\s+')

HELP_TEXT = """
GzirBotը պարբերաբար ստուգում է ՀԷՑ-ի և Վեոլիայի կայքերը և հավաքում կոմունալ անջատումների մասին տվյալները:
Ավելացրու՜ քեզ հետաքրքրող փողոցների, գյուղերի, շրջանների անունները՝ օգտագործելով /add հրամանը և GzirBotը քեզ կուղարկի դրանց մասին բոլոր հայտարարությունները: 

Հասանելի հրամանները.

/add տեղանուններ
Տեղանունները պետք է բաժանված լինեն ստորակետերով:
Օրինակ: `/add նալբանդյան, տիգրան մեծ, փարպեցի, ուլնեցի`

/remove տեղանուններ
Տեղանունները պետք է բաժանված լինեն ստորակետերով:
Օրինակ: `/remove նալբանդյան, ազատություն, փարպեցի, ուլնեցի`

/show
Տեսնել իմ տեղանունները:

/help
Ցույց տալ մանրամասն նկարագրությունը և օգտվելու ձևը:

Հայտարարությունները վերցվում են հետևյալ կայքերից.

https://interactive.vjur.am
https://www.ena.am/Info.aspx?id=5
"""

UNKNOWN_COMMAND_TEXT = f'Unknown command.\n{HELP_TEXT}'

SEND_KEYWORDS_TO_ADD = """Ուղարկի՜ր տեղանուններ՝ ավելացնելու համար:"""

SEND_KEYWORDS_TO_REMOVE = """Ուղարկի՜ր տեղանուններ՝ հեռացնելու համար:"""

SHOW_KEYWORDS_TEXT = """
Քո տեղանունները.
{}
"""

NO_KEYWORDS_TEXT = 'Դու չես ավելացրել ոչ իմ տեղանուն'

KEYWORDS_ADDED_TEXT = 'Տեղանուններն ավելացված են'
KEYWORDS_REMOVED_TEXT = 'Տեղանունները հեռացված են'

KEYWORDS_INPUT_PLACEHOLDER = 'Օր. կոմիտաս, մաշտոց'
