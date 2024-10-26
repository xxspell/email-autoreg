import random

from core.utils.log import xlogger


def generate_afk_seconds(min_seconds: int = 3, max_seconds: int = 8) -> int:
    seconds = random.randint(min_seconds, max_seconds)
    xlogger.debug(f"Setting AFK duration to {seconds} seconds")
    return seconds

