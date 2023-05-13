import asyncio

from constants import updates_failure_timeout
from telegram.api import get_updates


async def start_receiving_updates(on_update):
    """
    This function will wait for updates from telegram infinitely.
    Whenever an update is received, on_update callback will be called and the update data will be passed as an argument.
    Long polling is used for getting updates.
    :param on_update:
    :return:
    """
    while True:
        updates = get_updates()
        if updates is None:
            await asyncio.sleep(updates_failure_timeout)
            continue

        on_update(updates)
