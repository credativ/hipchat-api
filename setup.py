#!/usr/bin/env python

from distutils.core import setup

setup(
    name='hipchat-api',
    version='1.0',
    description='A little abstraction layer for HipChat',
    author='Michael Sprengel',
    url='https://www.credativ.de',
    author_email='michael.sprengel@credativ.de',
    license='MIT',
    packages=['hipchat'],
    package_dir = { 'hipchat': 'src/hipchat' }
)
