import time

from constants import updates_failure_timeout

from telegram.update_handler import handle_updates
from telegram.api import get_updates

while True:
    updates = get_updates()
    if updates is None:
        time.sleep(updates_failure_timeout)
        continue

    handle_updates(updates)
