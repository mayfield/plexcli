"""
Media Service Command.
"""

from . import base


class List(base.PlexCommand):
    """ List media """

    name = 'ls'

    def run(self, args):
        sections = (self.serverapi.get('library', 'sections'))
        self.print_xml(sections)


class Test1(base.PlexCommand):
    """ Hah hahah . """

    name = 'test1'

    def setup_args(self, parser):
        self.add_argument('url')

    def run(self, args):
        sections = self.api.get(args.url)
        self.print_xml(sections)


media = base.PlexCommand(name='media', doc=__doc__)
media.add_subcommand(List, default=True)
media.add_subcommand(Test1)

__commands__ = [media]
