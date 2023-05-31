import re

UPDATES_POLLING_TIMEOUT = 60
UPDATES_FAILURE_TIMEOUT = 10

UPDATE_INTERRUPTIONS_INTERVAL = 5 * 60

DAY_SECONDS = 60 * 60 * 24
INTERRUPTION_LIFESPAN = DAY_SECONDS

WHITESPACES_PATTERN = re.compile(r'\s+')

HELP_TEXT = """
GzirBot scrapes veolias site every 5 minutes to get information about water interruption announcements.
Announcement text will be forwarded to you if it contains any of your specified keywords.
The bot is, however, not smart enough and if you add a street name, but it's conjugated in the announcement, the bot won't notify you.
E.g. announcements with words ուլնեցու, լոռվա, won't be forwarded if your keywords are ուլնեցի, լոռի, so you can add keywords ուլնեց and լոռ instead.
To add or remove keywords, please don't tap on /add or /remove links. Type manually and send as message. E.g. /add Նալբանդյան

Here is the list of available commands:

/add keywords
Keywords should be separated by commas.
Example: `/add Նալբանդյան, Ա.Ահարոնյան, Փարպեցի`

/remove keywords
Keywords should be separated by commas.
Example: `/add Նալբանդյան, Ա.Ահարոնյան, Փարպեցի`

/show
This will show current keywords you are subscribed to.

/help
Show help text

All the announcements data is scraped from: https://interactive.vjur.am
"""

UNKNOWN_COMMAND_TEXT = f'Unknown command.\n{HELP_TEXT}'

KEYWORDS_NOT_SPECIFIED_TEXT = """No keywords are specified.

Please don't tap on the command in bots command list.

Type manually and send as message. E.g.
 /add կոմիտաս, ազատությ
 """

SHOW_KEYWORDS_TEXT = """
Here are the keywords you are subscribed to:
{}
"""

NO_KEYWORDS_TEXT = 'You are not subscribed to any keywords'

KEYWORDS_ADDED_TEXT = 'Keywords added'
KEYWORDS_REMOVED_TEXT = 'Keywords removed'

