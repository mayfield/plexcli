"""
Interactive shell for Plex.
"""

import code
import shellish


class PlexShell(shellish.Shell):

    intro = '\n'.join([
        'Welcome to the Plex shell.',
        'Type "help" or "?" to list commands and "exit" to quit.'
    ])

    @property
    def prompt(self):
        auth_state = self.root_command.state['auth']
        info = {
            "user": auth_state['username'],
            "site": self.api.site.split('//', 1)[1],
            "cwd": '/'.join(self.cwd)
        }
        return ': \033[7m%(user)s\033[0m@%(site)s /%(cwd)s ; \n:; ' % (info)

    def __init__(self, root_command):
        super().__init__(root_command)
        self.api = root_command.api
        self.api = root_command.api
        self.cwd = []

    def do_ls(self, arg):
        if arg:
            parent = self.api.get_by_id_or_name('accounts', arg)
        else:
            parent = self.cwd[-1]
        items = []
        for x in self.api.get_pager('accounts', account=parent['id']):
            items.append('%s/' % x['name'])
        for x in self.api.get_pager('routers', account=parent['id']):
            items.append('r:%s' % x['name'])
        account_filter = {"profile.account": parent['id']}
        for x in self.api.get_pager('users', **account_filter):
            items.append('u:%s' % x['username'])
        self.columnize(items)

    def do_debug(self, arg):
        """ Run an interactive python interpretor. """
        code.interact(None, None, self.__dict__)

    def do_cd(self, arg):
        cwd = self.cwd[:]
        if arg.startswith('/'):
            del cwd[1:]
        for x in arg.split('/'):
            if not x or x == '.':
                continue
            if x == '..':
                cwd.pop()
            else:
                newdir = self.get_account(x, parent=cwd[-1])
                if not newdir:
                    print("Account not found:", x)
                    return
                cwd.append(newdir)
        self.cwd = cwd

    def get_account(self, id_or_name, parent=None):
        options = {}
        if parent is not None:
            options['account'] = parent['id']
        newdir = self.api.get_by_id_or_name('accounts', id_or_name,
                                            required=False, **options)
        return newdir
