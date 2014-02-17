version = VERSION = __version__ = '0.0.1'
import debris

from .handler import TorndownHandler

def clear():
    """Simply clear all torndown data.
    Each page will rebuild on their own.
    """
    debris.cachier.remove("torndown://*")
