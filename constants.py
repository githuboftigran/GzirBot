import re

updates_polling_timeout = 60
updates_failure_timeout = 10

update_interruptions_interval = 60 * 60

day_seconds = 60 * 60 * 24
interruption_lifespan = day_seconds

whitespaces_pattern = re.compile(r"\s+")

help_text = """
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

unknown_command_text = f'Unknown command.\n{help_text}'

show_keywords_text = """
Here are the keywords you are subscribed to:
{}
"""

no_keywords_text = 'You are not subscribed to any keywords'

keywords_added_text = 'Keywords added'
keywords_removed_text = 'Keywords removed'

