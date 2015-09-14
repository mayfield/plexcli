"""
Interactive shell for Plex.
"""

import code
import humanize
import re
import shellish
from datetime import datetime


class PlexShell(shellish.Shell):

    default_prompt_format = r': \033[7m{user}\033[0m@{server} /{cwd} ; \n:;'
    intro = '\n'.join([
        'Welcome to the Plex shell.',
        'Type "help" or "?" to list commands and "exit" to quit.'
    ])

    def prompt_info(self):
        state = self.root_command.state
        info = super().prompt_info()
        info.update( {
            "user": state['auth']['username'],
            "server": state.get('server_name', '<offline>'),
            "cwd": '/'.join(self.cwd_titles)
        })
        return info

    def __init__(self, root_command):
        super().__init__(root_command)
        self.cloudapi = root_command.cloudapi
        self.serverapi = root_command.serverapi
        self.cwd = []
        self.cwd.append(('library/sections', 'Sections'))

    @property
    def cwd_titles(self):
        return [x[1] for x in self.cwd]

    @property
    def cwd_keys(self):
        return self.flatten_dir(self.cwd)

    def flatten_dir(self, directory):
        url = []
        for x in directory:
            if x[0].startswith('/'):
                del url[:]
                part = x[0][1:]
            else:
                part = x[0]
            url.append(part)
        return url

    def seek_dir(self, path):
        directory = self.cwd[:]
        if path[0].startswith('/'):
            del directory[1:]
        for x in path:
            if not x or x == '.':
                continue
            if x == '..':
                directory.pop()
            else:
                section = self.serverapi.get(*self.flatten_dir(directory))
                el = self.get_dir(section, x)
                if el is None:
                    raise SystemExit("Directory Not Found: %s" % x)
                directory.append((el.get('key'), self.get_title(el)))
        return directory

    def get_title(self, el):
        """ Make the title more CLI friendly. """
        title = re.sub('''['"`]''', '', el.get('title'))
        return title.replace(' ', '_')

    def do_ls(self, arg):
        verbose = '-l' in arg
        items = []
        section = self.serverapi.get(*self.cwd_keys)
        if verbose:
            items.append(['Title', 'Year', 'Added', 'Type', 'Duration'])
        for x in section:
            if verbose:
                if x.tag == 'Directory':
                    items.append([self.get_title(x), '', '', 'dir', ''])
                elif x.tag == 'Video':
                    added = datetime.fromtimestamp(int(x.get('addedAt')))
                    mins = round(int(x.get('duration')) / 60000)
                    items.append([self.get_title(x), x.get('year'),
                                  humanize.naturaltime(added), x.get('type'),
                                  '%s mins' % mins])
                else:
                    raise SystemExit("What is this?: %s" % x)
            else:
                if x.tag == 'Directory':
                    items.append('%s/' % self.get_title(x))
                elif x.tag == 'Video':
                    items.append(self.get_title(x))
                else:
                    raise SystemExit("What is this?: %s" % x)
        if verbose:
            self.tabulate(items)
        else:
            self.columnize(items)

    def do_pwd(self, arg):
        print('%s/%s' % (self.serverapi.uri, '/'.join(self.cwd_keys)))

    def do_debug(self, arg):
        """ Run an interactive python interpretor. """
        env = self.__dict__.copy()
        root = self.root_command
        env.update((x, getattr(root, x)) for x in root.context_keys)
        code.interact(None, None, env)

    def get_dir(self, section, title):
        for x in section.iter('Directory'):
            if self.get_title(x) == title:
                return x

    def do_cd(self, arg):
        self.cwd = self.seek_dir(arg.split('/'))

    def complete_cd(self, _ignore, line, begin, end):
        prefix = line.split('cd ', 1)[1]
        path = prefix.split('/')
        if len(path) > 1:
            offt = self.seek_dir(path[:-1])
        else:
            offt = self.cwd
        section = self.serverapi.get(*self.flatten_dir(offt))
        dirs = section.iter('Directory')
        titles = [self.get_title(x) for x in dirs]
        return ['%s/' % x for x in titles if x.startswith(path[-1])]
