#!/usr/bin/env python

from distutils.core import setup

setup(
    name='hipchat-api',
    version='1.0',
    description='A little abstraction layer for HipChat',
    author='Michael Sprengel',
    author_email='michael.sprengel@credativ.de',
    packages=['hipchat'],
    package_dir = { 'hipchat': 'src/hipchat' }
)
