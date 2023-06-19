import re

UPDATES_POLLING_TIMEOUT = 60
UPDATES_FAILURE_TIMEOUT = 60

UPDATE_INTERRUPTIONS_INTERVAL = 5 * 60

DAY_SECONDS = 60 * 60 * 24
INTERRUPTION_LIFESPAN = DAY_SECONDS

WHITESPACES_PATTERN = re.compile(r'\s+')

HELP_TEXT = """
GzirBot scrapes Veolia Jurs and ENAs (Electric Networks of Armenia) sites every 5 minutes to get information about utility interruption announcements.
Add your street (or village / district / area) name and GzirBot will forward the announcements, which contain your specified keywords to you.

Here is the list of available commands:

/add keywords
Keywords should be separated by commas.
Example: `/add նալբանդյան, ազատություն, փարպեցի, ուլնեցի`

/remove keywords
Keywords should be separated by commas.
Example: `/remove նալբանդյան, ազատություն, փարպեցի, ուլնեցի`

/show
Show current keywords you are subscribed to.

/help
Show help text

All the announcements data is scraped from these pages:
https://interactive.vjur.am
https://www.ena.am/Info.aspx?id=5
"""

UNKNOWN_COMMAND_TEXT = f'Unknown command.\n{HELP_TEXT}'

KEYWORDS_NOT_SPECIFIED_TEXT = """No keywords are specified.

Please don't tap on the command in bots command list.

Type manually and send as message. E.g.
 /add կոմիտաս, ազատություն
 """

SEND_KEYWORDS_TO_ADD = """Type keywords you want to add"""

SEND_KEYWORDS_TO_REMOVE = """Type keywords you want to remove"""

SHOW_KEYWORDS_TEXT = """
Here are the keywords you are subscribed to:
{}
"""

NO_KEYWORDS_TEXT = 'You are not subscribed to any keywords'

KEYWORDS_ADDED_TEXT = 'Keywords added'
KEYWORDS_REMOVED_TEXT = 'Keywords removed'

KEYWORDS_INPUT_PLACEHOLDER = 'E.g. կոմիտաս, մաշտոց, ազատություն'
