"""
Media Service Command.
"""

from . import base


class List(base.PlexCommand):
    """ List media """

    name = 'ls'

    def run(self, args):
        sections = (self.api.get('library', 'sections'))
        self.print_xml(sections)

media = base.PlexCommand(name='media', doc=__doc__)
media.add_subcommand(List, default=True)

__commands__ = [media]
