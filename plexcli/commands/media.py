"""
Media Service Command.
"""

from . import base
from .. import util


class List(base.PlexCommand):
    """ List media """

    name = 'ls'

    def run(self, args):
        sections = (self.serverapi.get('library', 'sections'))
        self.print_xml(sections)


class Refresh(base.PlexCommand):
    """ Refresh (rescan) media """

    name = 'refresh'

    def setup_args(self, parser):
        self.add_argument('section', nargs='?',
                          complete=self.complete_section)

    def get_sections(self):
        return dict((util.friendly_get(x, 'title'), x.attrib)
                    for x in self.serverapi.get('library', 'sections'))

    def complete_section(self, start):
        sections = self.get_sections()
        return set(x for x in sections if x.startswith(start))

    def run(self, args):
        path = ['library', 'sections']
        if args.section:
            sections = self.get_sections()
            if args.section not in sections:
                raise SystemExit("Section not found: %s" % args.section)
            path.append(sections[args.section]['key'])
        path.append('refresh')
        self.serverapi.get(*path)


media = base.PlexCommand(name='media', doc=__doc__)
media.add_subcommand(List, default=True)
media.add_subcommand(Refresh)

__commands__ = [media]
