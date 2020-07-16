from datetime import datetime
import logging

from pyappcache.keys import GenericStringKey


class UserToLastChangedKey(GenericStringKey[datetime]):
    def __init__(self, username: str):
        self._username = username

    def as_segments(self):
        return [self._username, "last_changed"]


class UserFavouritePokemon(GenericStringKey[str]):
    def __init__(self, username: str):
        self._username = username

    def namespace_key(self):
        return UserToLastChangedKey(self._username)

    def as_segments(self):
        return ["favourite_pokemon"]


def test_namespace_get_when_no_namespace(cache):
    key = UserFavouritePokemon("john")

    cache.set(key.namespace_key(), datetime(2018, 1, 3))
    cache.set(key, "pikachu")
    cache.invalidate(key.namespace_key())
    assert cache.get(key) is None


def test_namespace_set_when_no_namespace(cache):
    key = UserFavouritePokemon("john")

    cache.set(key, "pikachu")
    assert cache.get(key) is None


def test_namespace_get_and_set_when_namespace_present(cache):
    key = UserFavouritePokemon("john")

    cache.set(key.namespace_key(), datetime(2018, 1, 3))
    cache.set(key, "pikachu")

    assert cache.get(key) == "pikachu"


def test_get_and_set_when_namespace_outdated(cache):
    key = UserFavouritePokemon("john")

    cache.set(key.namespace_key(), datetime(2018, 1, 3))
    cache.set(key, "pikachu")
    cache.set(key.namespace_key(), datetime(2018, 1, 4))

    assert cache.get(key) is None


def test_get_and_set_when_namespace_updated(cache):
    key = UserFavouritePokemon("john")

    cache.set(key.namespace_key(), datetime(2018, 1, 3))
    cache.set(key, "pikachu")
    cache.set(key.namespace_key(), datetime(2018, 1, 4))
    cache.set(key, "bulbasaur")

    assert cache.get(key) == "bulbasaur"


def test_invalidation_when_no_namespace(cache, caplog):
    key = UserFavouritePokemon("john")

    with caplog.at_level(logging.WARNING, logger="pyappcache.cache"):
        cache.invalidate(key)
        assert caplog.record_tuples == [
            (
                "pyappcache.cache",
                30,
                "unable to invalidate key as namespace does not exist",
            )
        ]


def test_invalidation_when_namespace_present(cache):
    key = UserFavouritePokemon("john")

    cache.set(key.namespace_key(), datetime(2018, 1, 3))
    cache.set(key, "pikachu")

    cache.invalidate(key)
    assert cache.get(key) is None
