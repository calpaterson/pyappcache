import random
import string


def random_string() -> str:
    return "".join(random.choice(string.ascii_lowercase) for _ in range(32))
