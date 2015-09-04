"""
Foundation components for commands.
"""

import shellish
from plexcli import shell
from xml.etree import ElementTree


class PlexCommand(shellish.Command):
    """ Extensions for dealing with Plex's APIs. """

    Shell = shell.PlexShell

    def print_xml(self, xml):
        """ Debug function to print a text repr of an ElementTree. """
        ElementTree.dump(xml)
