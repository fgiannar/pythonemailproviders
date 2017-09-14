# -*- coding: utf-8 -*-

"""
helpers
~~~~~~~~~~~~~~~~~

This module contains various helper functions
"""

import requests


def _make_request(**kwargs):
    try:
        res = requests.request(**kwargs)
    except requests.exceptions.RequestException as e:
        raise e
    else:
        res.raise_for_status()
    return res.json()
