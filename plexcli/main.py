"""
Bootstrap the shell and commands and then run either one.
"""

import getpass
import importlib
import json
import os.path
import pkg_resources
import sys
from . import api
from .commands import base

command_modules = [
    'media',
    'servers',
    'clients',
    'sessions',
    'activity'
]


class State(dict):
    """ Stateful dict, writes to disk on updates. """

    def __init__(self, filename):
        self.filename = filename
        try:
            with open(self.filename) as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}
        super().__init__(data)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        with open(self.filename, 'w') as f:
            json.dump(self, f, indent=4)

state = State(os.path.expanduser('~/.plex_state'))


class PlexRoot(base.PlexCommand):
    """ Plex Command Line Interface

    This utility represents a collection of sub-commands to perform against
    the Plex service ecosystem.  You must already have a valid Plex account
    to use this tool.  For more info go to https://plex.tv/. """

    name = 'plex'

    def setup_args(self, parser):
        distro = pkg_resources.get_distribution('plexcli')
        self.add_argument('--username')
        self.add_argument('--password')
        self.add_argument('--auth_token')
        self.add_argument('--site', default='https://plex.tv')
        self.add_argument('--version', action='version',
                          version=distro.version)

    def run(self, args):
        self.interact()


def get_auth_params(args):
    """ Return the required minimum params for plex auth. """
    # Look for argument overrides, state, and lastly prompt the user.
    if args.auth_token:
        return {"auth_token": args.auth_token}
    elif args.username:
        return {
            "username": args.username,
            "password": args.password or getpass.getpass()
        }
    elif state.get('auth'):
        return {"auth_token": state['auth']['token']}
    else:
        return {
            "username": input('Username/email: '),
            "password": getpass.getpass()
        }


def main():
    cloudapi = api.PlexService(state)
    serverapi = api.PlexService(state)
    root = PlexRoot(cloudapi=cloudapi, serverapi=serverapi, state=state)
    for modname in command_modules:
        module = importlib.import_module('.%s' % modname, 'plexcli.commands')
        for command in module.__commands__:
            root.add_subcommand(command)
    args = root.argparser.parse_args()
    auth_params = get_auth_params(args)
    cloudapi.connect(args.site, **auth_params)
    if state.get('server_urls'):
        try:
            serverapi.multi_connect(state['server_urls'],
                                    auth_token=state['server_auth_token'])
        except IOError as e:
            print(e)
    try:
        root(args)
    except KeyboardInterrupt:
        sys.exit(1)
