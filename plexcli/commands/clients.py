"""
Client display.
"""

from . import base
from shellish.layout import Table


class List(base.PlexCommand):
    """ List clients """

    name = 'ls'

    def run(self, args):
        clients = self.serverapi.get('clients').findall('Server')
        headers = ['Name', 'Host', 'Product', 'Class', 'Capabilities']
        getcaps = lambda x: ', '.join(x['protocolCapabilities'].split(','))
        accessors = ['name', 'host', 'product', 'deviceClass', getcaps]
        t = Table(headers=headers, accessors=accessors)
        t.print([x.attrib for x in clients])


clients = base.PlexCommand(name='clients', doc=__doc__)
clients.add_subcommand(List, default=True)

__commands__ = [clients]
