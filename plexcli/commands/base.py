"""
Foundation components for commands.
"""

import fnmatch
import re
import shellish
from plexcli import shell
from xml.etree import ElementTree


class PlexCommand(shellish.Command):
    """ Extensions for dealing with Plex's APIs. """

    Shell = shell.PlexShell

    def xml_as_string(self, xml):
        return ElementTree.tostring(xml)

    def friendly_str(self, value):
        """ Make a string more CLI friendly. """
        value = re.sub('''['"`']''', '', value)
        return value.replace(' ', '_')

    def friendly_get(self, item, attrname, default=None):
        """ Get and cleanup an xml attribute. """
        return self.friendly_str(item.get(attrname, default))

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

    def fetch_section(self, directory):
        """ Fetch a section from the server api at .directory offset. """
        return self.serverapi.get(*self.flatten_dir(directory))

    def find_dir(self, section, pattern):
        """ Get a directory by title with support for glob patterns. """
        for x in section.iter('Directory'):
            if fnmatch.fnmatch(self.friendly_get(x, 'title'), pattern):
                return x

    def seek_dir(self, path):
        directory, remainder = self.try_seek_dir(path)
        if remainder:
            raise SystemExit("Directory Not Found: %s" % remainder[0])
        return directory

    def try_seek_dir(self, path):
        directory = self.cwd[:]
        if not path[0]:
            del directory[1:]
        for i, x in enumerate(path):
            if not x or x == '.':
                continue
            if x == '..':
                directory.pop()
            else:
                section = self.fetch_section(directory)
                el = self.find_dir(section, x)
                if el is None:
                    break
                directory.append((el.get('key'),
                                  self.friendly_get(el, 'title')))
        return directory, path[i:]
