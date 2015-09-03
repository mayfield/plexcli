"""
Foundation components for commands.
"""

import shellish
from plexcli import shell


class PlexCommand(shellish.Command):
    """ Extensions for dealing with Plex's APIs. """

    Shell = shell.PlexShell
