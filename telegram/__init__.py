import asyncio

from constants import updates_failure_timeout
from api import get_updates


async def start_receiving_updates(on_update):
    while True:
        updates = get_updates()
        if updates is None:
            await asyncio.sleep(updates_failure_timeout)
            continue

        on_update(updates)
