"""
Interactive shell for Plex.
"""

import shellish
from . import util


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
            "server": util.friendly_get(state, 'server_name', '<offline>'),
            "cwd": '/'.join(self.root_command.cwd_titles)
        })
        return info
