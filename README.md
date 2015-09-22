plexcli
===========
_*CLI for Plex*_

[![Maturity](https://img.shields.io/pypi/status/plexcli.svg)](https://pypi.python.org/pypi/plexcli)
[![License](https://img.shields.io/pypi/l/plexcli.svg)](https://pypi.python.org/pypi/plexcli)
[![Change Log](https://img.shields.io/badge/change-log-blue.svg)](https://github.com/mayfield/plexcli/blob/master/CHANGELOG.md)
[![Build Status](https://semaphoreci.com/api/v1/projects/5c2797d3-7839-4176-a14f-be1ed80a06f2/547084/shields_badge.svg)](https://semaphoreci.com/mayfield/plexcli)
[![Version](https://img.shields.io/pypi/v/plexcli.svg)](https://pypi.python.org/pypi/plexcli)


About
--------

Installation provides a command line utility (plex) which can be used to
interact with Plex services.  Commands are subtasks of the plex utility.
The full list of subtasks are visible by running 'plex --help'.


Requirements
--------

* syndicate Python Library
* humanize Python Library
* Plex Account
* Plex Server [and/or Client (soon)]


Installation
--------

**PyPi Stable Release**

```
pip3 install plexcli
```
    
**Development Release**

```
python3 ./setup.py build
python3 ./setup.py install
```

*or*

```
python3 ./setup.py develop
```


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
