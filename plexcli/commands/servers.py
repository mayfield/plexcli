"""
List and manage plex servers linked to your account.
"""

from . import base
from .. import util


class List(base.PlexCommand):
    """ List servers """

    name = 'ls'

    def run(self, args):
        data = [['Name', 'Address', 'Local Address', 'Owned']]
        data.extend([
            util.friendly_get(x, 'name'),
            '%s://%s:%s' % (x.attrib['scheme'],
                            x.attrib['address'],
                            x.attrib['port']),
            '%s://%s:32400' % (x.attrib['scheme'],
                               x.attrib['localAddresses']),
            bool(int(x.attrib['owned']))
        ] for x in self.cloudapi.get('pms', 'servers'))
        self.tabulate(data)


class Select(base.PlexCommand):
    """ Select the default server for commands to run against. """

    name = 'select'

    def setup_args(self, parser):
        self.add_argument('server', complete=self.servers_complete)

    def servers_complete(self, startswith):
        return set(util.friendly_get(x, 'name')
                   for x in self.cloudapi.get('pms', 'servers'))

    def run(self, args):
        servers = dict((util.friendly_get(x, 'name'), x.attrib)
                       for x in self.cloudapi.get('pms', 'servers'))
        try:
            server = servers[args.server]
        except KeyError:
            raise SystemExit("Server Not Found: %s" % args.server)
        urls = [
            '%s://%s:32400' % (server['scheme'], server['localAddresses']),
            '%s://%s:%s' % (server['scheme'], server['address'],
                            server['port'])
        ]
        api = self.serverapi
        api.multi_connect(urls, verbose=True,
                          auth_token=server['accessToken'])
        self.state['server_urls'] = urls
        self.state['server_name'] = util.friendly_get(server, 'name')
        self.state['server_auth_token'] = server['accessToken']
        if self.shell:
            del self.shell.cwd[1:]


servers = base.PlexCommand(name='servers', doc=__doc__)
servers.add_subcommand(List, default=True)
servers.add_subcommand(Select)

__commands__ = [servers]
