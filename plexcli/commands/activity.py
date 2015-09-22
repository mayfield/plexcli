"""
Activity logs.
"""

import asyncio
import datetime
import json
import websockets
from . import base
from shellish.layout import Table


class Log(base.PlexCommand):
    """ Show activity log """

    name = 'log'
    type_map = {
        'StatusNotification': 'Status',
        'ProgressNotification': 'Progress'
    }

    @asyncio.coroutine
    def notifications(self, table):
        server = self.serverapi.uri.split('://', 1)[1]
        notif_url = 'ws://%s/:/websockets/notifications' % server
        feed = yield from websockets.connect(notif_url)
        while True:
            data = yield from feed.recv()
            if data is None:
                break
            table.print(json.loads(data).get('_children'))
        yield from feed.close()

    def get_ts(self, obj):
        return datetime.datetime.now().strftime('%I:%M:%S %p')

    def get_type(self, obj):
        return self.type_map[obj['_elementType']]

    def get_msg(self, obj):
        if 'message' in obj:
            return obj['message']
        return '%s: %s' % (obj['title'], obj['description'])

    def run(self, args):
        headers = ['Date', 'Type', 'Message']
        accessors = [self.get_ts, self.get_type, self.get_msg]
        columns = [11, 8, None]
        table = Table(columns=columns, headers=headers, accessors=accessors,
                      flex=False)
        evloop = asyncio.get_event_loop()
        evloop.run_until_complete(self.notifications(table))


activity = base.PlexCommand(name='activity', doc=__doc__)
activity.add_subcommand(Log, default=True)

__commands__ = [activity]
