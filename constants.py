import re

UPDATES_POLLING_TIMEOUT = 60
UPDATES_FAILURE_TIMEOUT = 10

UPDATE_INTERRUPTIONS_INTERVAL = 60 * 60

DAY_SECONDS = 60 * 60 * 24
INTERRUPTION_LIFESPAN = DAY_SECONDS

WHITESPACES_PATTERN = re.compile(r'\s+')

HELP_TEXT = """
Here are the following commands available:

/help
Show help menu

/add keywords
Keywords should be separated by commas.
Example: `/add Նալբանդյան, Ա.Ահարոնյան, Փարպեցի`

/remove keywords
Keywords should be separated by commas.
Example: `/add Նալբանդյան, Ա.Ահարոնյան, Փարպեցի`

/show
This will show current keywords you are subscribed to.

All the data is taken from: https://interactive.vjur.am/
"""

UNKNOWN_COMMAND_TEXT = f'Unknown command.\n{HELP_TEXT}'

SHOW_KEYWORDS_TEXT = """
Here are the keywords you are subscribed to:
{}
"""

NO_KEYWORDS_TEXT = 'You are not subscribed to any keywords'

KEYWORDS_ADDED_TEXT = 'Keywords added'
KEYWORDS_REMOVED_TEXT = 'Keywords removed'

