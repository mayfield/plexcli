"""
Shell (interactive) tools mostly related to navigation.
"""

import code
import humanize
import os.path
from datetime import datetime
from . import base


class ChangeDir(base.PlexCommand):
    """ Change the current working directory. """

    name = 'cd'

    def setup_args(self, parser):
        self.add_argument('dir', complete=self.complete_dir)

    def run(self, args):
        path = os.path.normpath(args.dir).split('/')
        self.cwd[:] = self.seek_dir(path)

    def complete_dir(self, prefix):
        path = prefix.split('/')
        directory = self.seek_dir(path[:-1]) if len(path) > 1 else self.cwd
        dirs = self.fetch_section(directory).iter('Directory')
        titles = [self.friendly_get(x, 'title') for x in dirs]
        return set('%s/' % x for x in titles if x.startswith(path[-1]))


class List(base.PlexCommand):
    """ List contents of a directory. """

    name = 'ls'

    def setup_args(self, parser):
        self.add_argument('-l', '--long', dest='verbose', action='store_true',
                          help='Long listing (verbose) of contents.')
        self.add_argument('-r', '--reverse', action='store_true',
                          help='Reverse the sort order.')
        sort_group = parser.add_argument_group('sort options')
        sorters = sort_group.add_mutually_exclusive_group()
        sorters.add_argument('-U', '--creationsort', action='store_true',
                             help='Sort output by creation time (release ' \
                                  'date).')
        sorters.add_argument('-t', '--addedsort', action='store_true',
                             help='Sort output by add time.')
        sorters.add_argument('-S', '--sizesort', action='store_true',
                             help='Sort output by size')
        self.add_argument('file_or_dir', metavar="FILE_OR_DIR", nargs='?')

    def run(self, args):
        if args.file_or_dir:
            path = os.path.normpath(args.file_or_dir).split('/')
            directory, remainder = self.try_seek_dir(path)
        else:
            directory = self.cwd
        section = self.fetch_section(directory)
        if args.verbose:
            items = [['Title', 'Year', 'Added', 'Type', 'Duration']]
            items.extend(self.verbose_collect(section))
            self.tabulate(items, columns=[None, None, None,
                          {"align": "right"}])
        else:
            self.columnize(self.terse_collect(section))

    def verbose_collect(self, section):
        items = []
        for x in section:
            if x.tag == 'Directory':
                items.append([self.friendly_get(x, 'title'), '', '', 'dir',
                              ''])
            elif x.tag == 'Video':
                added = datetime.fromtimestamp(int(x.get('addedAt')))
                mins = round(int(x.get('duration')) / 60000)
                items.append([self.friendly_get(x, 'title'), x.get('year'),
                              humanize.naturaltime(added), x.get('type'),
                              '%s mins' % mins])
            else:
                raise SystemExit("What is this?: %s" % x)
        return items

    def terse_collect(self, section):
        items = []
        for x in section:
            if x.tag == 'Directory':
                items.append('%s/' % self.friendly_get(x, 'title'))
            elif x.tag == 'Video':
                items.append(self.friendly_get(x, 'title'))
            else:
                raise SystemExit("What is this?: %s" % x)
        return items


class PrintWorkingDir(base.PlexCommand):
    """ Print the current working directory. """

    name = 'pwd'

    def run(self, args):
        print('%s/%s' % (self.serverapi.uri, '/'.join(self.cwd_keys)))


class Debug(base.PlexCommand):
    """ Run an interactive python interpretor. """

    name = 'debug'

    def run(self, args):
        env = self.__dict__.copy()
        root = self.root_command
        env.update((x, getattr(root, x)) for x in root.context_keys)
        code.interact(None, None, env)


__commands__ = [List]
__interactive_commands__ = [ChangeDir, PrintWorkingDir, Debug]
