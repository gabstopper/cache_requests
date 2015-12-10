#!/usr/bin/env python
# coding=utf-8
"""
==============
cache_requests
==============

**Simple. Powerful. Persistent LRU caching for the requests library.**

"""
from __future__ import absolute_import

import logging

from ._compat import NullHandler
from .memoize import memoize, RedisMemoize
from .sessions import Session

logging.getLogger(__name__).addHandler(NullHandler())

__author__ = 'Manu Phatak'
__email__ = 'bionikspoon@gmail.com'
__version__ = '1.0.0'
__all__ = ['config', 'Session', 'memoize', 'RedisMemoize', ]
