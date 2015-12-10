#!/usr/bin/env python
# coding=utf-8
"""
cache_requests.config
~~~~~~~~~~~~~~~~~~~~~~

Global config, default settings.

These are all easily overridden following python scope rules. Hierarchy: instance variables > class variables > config settings > environment variable settings.

.. note ::

    Environment variables are all caps prefixed with ``REDIS_``

"""
from __future__ import absolute_import

from functools import partial
from os import environ, path
from tempfile import gettempdir

from redislite import StrictRedis

temp_file = partial(path.join, gettempdir())

__all__ = ['ex', 'dbfilename', 'connection']

ex = environ.get('REDIS_EX', 60 * 60)  # 1 hour
dbfilename = environ.get('REDIS_DBFILENAME', temp_file('cache_requests.redislite'))
connection = environ.get('REDIS_CONNECTION') or partial(StrictRedis, dbfilename=dbfilename)
