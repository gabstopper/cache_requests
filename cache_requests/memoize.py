#!/usr/bin/env python
# coding=utf-8
"""
memoize module
--------------

This module implements a basic LRU decorator that syncs calls with a redislite database.
"""
from __future__ import absolute_import
import copy
import functools
import logging

from cache_requests import config

try:
    # noinspection PyPep8Naming
    import cPickle as pickle  # PY2X
except ImportError:
    import pickle
import redislite



log = logging.getLogger(__name__)


def make_hash(obj):
    """
    Recursively hash nested mixed objects (dicts, lists, other).


    :rtype : int
    :param object obj: an object
    :return: hash representation of the object
    """
    if isinstance(obj, (set, tuple, list)):
        return tuple(make_hash(item) for item in obj if item)
    elif not isinstance(obj, dict):
        return hash(obj)
    else:
        copied_obj = copy.deepcopy(obj)
        for k, v in copied_obj.items():
            copied_obj[k] = make_hash(v)

        return hash(tuple(frozenset(sorted(copied_obj.items()))))


class Memoize(object):
    """
    Decorator Class.  Standard LRU. With redis key/value caching.
    """

    _redis_connection = config.REDIS_CONNECTION or redislite.StrictRedis(
        dbfilename=config.REDISLITE_DB)

    _redis_expiration = config.EXPIRATION

    def __init__(self, function):
        self.function = function
        functools.update_wrapper(self, function)

    @property
    def redis(self):
        """
        Get redis connection string.

        :return: redis connection handle
        """
        return self.__class__._redis_connection

    def __getitem__(self, item):
        """
        Query db for key, de-pickle results.

        :rtype : object
        :param item: tuple of hashed args and kwargs
        :return: object from storage
        """
        value = self.redis.get(item)

        return None if not value else pickle.loads(value)

    def __setitem__(self, key, value):
        """
        Store a pickled object in the db.

        :param key: hash key
        :param object value: object to store
        """
        self.redis.set(name=key, value=pickle.dumps(value),
                       ex=self.__class__._redis_expiration)


    def __call__(self, *args, **kwargs):
        """
        Wrap :attr:`self.function`

        :param args: Arguments passed to decorated function
        :param kwargs: Keyword Arguments passed to decorated function
        :return: function results
        """

        #: hashed tuple of args and kwargs
        memo_key = make_hash((args, kwargs))

        # if no record in db, create a record
        if not self[memo_key]:
            self[memo_key] = self.function(*args, **kwargs)
            log.info('Caching results for hash: %s ', memo_key)
        else:
            log.debug('Results from cache hash: %s', memo_key)
        return self[memo_key]
