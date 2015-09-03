plexcli - CLI for Plex
===========

Installation provides a command line utility (plex) which can be used to
interact with Plex services.  Commands are subtasks of the plex utility.
The full list of subtasks are visible by running 'plex --help'.

**[CHANGELOG](CHANGELOG.md)**


Requirements
--------

* Syndicate Python Library
* humanize Python Library
* Plex Account
* Plex Server [and/or Client (soon)]


Installation
--------

    python3 ./setup.py build
    python3 ./setup.py install

or

    pip3 install plexcli


Compatibility
--------

* Python 3.4+


Mac OSX Notes
--------

I feel compelled to make a note about OSX as I've decided to only support
Python 3.4+ for this tool.  In my experience, using Python 3 as installed by
Homebrew and setuptools as installed by pip, a usable PATH is not provided
and/or symlinking behavior for python3 setuptools scripts is not handled.

To work around this I'm simply adding the 'bin' directory used for the Python
3 framework to my PATH variable, a la..

```shell
PATH=$PATH:/usr/local/Cellar/python3/3.4.2_1/Frameworks/Python.framework/Versions/3.4/bin
```

I welcome someone explaining to me a better solution.
