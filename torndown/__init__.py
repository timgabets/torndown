version = VERSION = __version__ = '0.0.1'

import debris

from torndown.handler import TorndownHandler

def clear():
    """Simply clear all torndown data.
    Each page will rebuild on their own.
    """
    debris.storage.remove("torndown:*")
