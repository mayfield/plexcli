"""
Common utility functions to be used by any plexcli components.
"""

import re


def friendly_str(value):
    """ Make a string more CLI friendly. """
    value = re.sub('''['"`']''', '', value)
    return value.replace(' ', '_')


def friendly_get(item, attrname, default=None):
    """ Get and cleanup an xml attribute. """
    return friendly_str(item.get(attrname, default))
