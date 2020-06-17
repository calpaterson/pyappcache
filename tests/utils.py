from typing import Optional
import re
import random
import string
import socket
from datetime import datetime, timedelta

from logging import getLogger

logger = getLogger(__name__)


def random_string() -> str:
    return "".join(random.choice(string.ascii_lowercase) for _ in range(32))


ONE_MEG = 1024 * 1024 * 1024

SLAB_REGEX = re.compile(br":(\d+):")


def get_memcache_ttl(key: bytes) -> Optional[int]:
    """There is no way to get the ttl of a key from pylibmc so we do it out of
    band with a socket via the text API."""
    logger.info("looking up the ttl of: %s", key)
    timelimit = datetime.utcnow() + timedelta(seconds=1)
    ttl_regex = re.compile(rb"ITEM %s \[[0-9]+ b; ([0-9]+) s]" % key, re.MULTILINE)

    attempt = 1
    # Looks like something is causing the IO to happen async so try for a second
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 11211))
    while datetime.utcnow() < timelimit:
        # 1. Get a list of slabs
        sock.send(b"stats items\r\n")
        response = sock.recv(ONE_MEG)
        slabs = set(int(slab) for slab in SLAB_REGEX.findall(response))

        # 2. Check every slab for our item
        for slab in slabs:
            command = bytes(f"stats cachedump {slab} 10\r\n", "utf-8")
            sock.send(command)
            response = sock.recv(ONE_MEG)
            match_obj = ttl_regex.search(response)
            if match_obj:
                ttl = int(match_obj.group(1))
                logger.info("found ttl for %s: %d (on attempt %d)", key, ttl, attempt)
                return ttl
        attempt += 1
    return None
