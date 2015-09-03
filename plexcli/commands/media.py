"""
Media Service Command.
"""

import sys
from . import base


class Formatter(object):

    def setup_args(self, parser):
        self.add_argument('-v', '--verbose', action='store_true')
        super().setup_args(parser)

    def prerun(self, args):
        self.formatter = self.verbose_formatter if args.verbose else \
                         self.terse_formatter
        super().prerun(args)

    def terse_formatter(self, account):
        return '%(name)s (id:%(id)s)' % account

    def verbose_formatter(self, account):
        count = dict.fromkeys(['routers', 'groups', 'user_profiles',
                               'subaccounts'], 0)
        for x in count:
            n = self.api.get(urn=account[x], count='id')[0]['id_count']
            account['%s_count' % x] = n
        return '%(name)s (id:%(id)s, routers:%(routers_count)d ' \
               'groups:%(groups_count)d, users:%(user_profiles_count)d, ' \
               'subaccounts:%(subaccounts_count)d)' % account

import xml.etree.ElementTree
xdump = xml.etree.ElementTree.dump

class List(Formatter, base.PlexCommand):
    """ List media """

    name = 'ls'

    def run(self, args):
        sections = (self.api.get('library', 'sections'))
        xdump(sections)
        servers = (self.api.get('pms', 'servers'))
        xdump(servers)
        import pdb
        pdb.set_trace()

media = base.PlexCommand(name='media', doc='Base Media Command')
media.add_subcommand(List, default=True)

__commands__ = [media]
