#!/usr/bin/env python

from setuptools import setup, find_packages

README = 'README.md'


def long_desc():
    try:
        import pypandoc
    except ImportError:
        with open(README) as f:
            return f.read()
    else:
        return pypandoc.convert(README, 'rst')

setup(
    name='plexcli',
    version='0.2.0',
    description='Command Line Interface for Plex',
    author='Justin Mayfield',
    author_email='tooker@gmail.com',
    url='https://github.com/mayfield/plexcli/',
    license='MIT',
    long_description=long_desc(),
    packages=find_packages(),
    install_requires=[
        'syndicate==1.2.0',
        'shellish>=0.5.8',
        'humanize'
    ],
    entry_points = {
        'console_scripts': ['plex=plexcli.main:main'],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
    ]
)
