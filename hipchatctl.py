#!/usr/bin/env python
# -------------------------------------------------------------------------------- #
# Copyright (c) 2017 Michael Sprengel for credativ GmbH
# www.credativ.de
#
# powered by Swisscom Health AG | www.swisscom.com/health
#
# This script is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This script was created to simplify the gathering of information about
# the VMs inside of VMWare vCloud but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You can find a copy of GNU General Public License by visiting
# <http://www.gnu.org/licenses/>.
# -------------------------------------------------------------------------------- #

#
# Include important modules
#
import argparse
import sys
import os
import json

from hipchat.api import HipchatAPI

#
# Global parameter
#
DEFAULT_CONFIG_FILE = 'hipchat.ini'

TYPE_MESSAGE = "msg"
TYPE_CARD = "card"
TYPE_HTML = "html"
TYPE_CHOICE_LIST = [TYPE_MESSAGE, TYPE_CARD, TYPE_HTML]

sys.tracebacklimit = 0

#
# This class defines the interface
# to send messages to hipchat
#
class HipchatControl(object):

    #----------------------------------------
    def __init__(self):
    #----------------------------------------
        self.arguments = None
        self.parse_cli()

        self.hipchat = HipchatAPI(self.arguments.config, room=self.arguments.room)
        self.proceed_arguments()

    #----------------------------------------
    def parse_cli(self):
    #----------------------------------------
        self.parser = argparse.ArgumentParser(description='Send messages to a Hipchat room.')
        self.parser.add_argument(
            'room',
            metavar='roomid',
            type=int,
            help='ID of the room you want to send a message to.'
        )
        self.parser.add_argument(
            'type',
            metavar='type',
            type=str,
            help='The type of message you want to send (Choices: %s)' % ', '.join(TYPE_CHOICE_LIST),
            choices = TYPE_CHOICE_LIST
        )
        self.parser.add_argument(
            'message',
            metavar='message',
            type=str,
            help='The message you want to send. If you have choosen card then this contains the card in JSON format.'
        )
        self.parser.add_argument(
            '--config',
            metavar='config',
            type=str,
            default=DEFAULT_CONFIG_FILE,
            help='Path to the config file you want to use.'
        )
        self.parser.add_argument(
            '--color',
            metavar='color',
            type=str,
            default="gray",
            help='Color of the background (e.g red, gray, yellow)'
        )
        self.arguments = self.parser.parse_args()

        if self.arguments.message == '-':
            self.arguments.message = sys.stdin.read()

    #----------------------------------------
    def proceed_arguments(self):
    #----------------------------------------
        if self.arguments.type == "msg":
            message = dict(
                color = self.arguments.color,
                message_format = "text",
                message = self.arguments.message
            )
            response_code = self.hipchat.send_message(message)

            print "Send message to room %d and Hipchat returned %d" % (self.arguments.room, response_code)
        elif self.arguments.type == "card":
            message = dict(
                color = self.arguments.color,
                message_format = "html",
                message = "Update card",
                card = json.loads(self.arguments.message)
            )
            response_code = self.hipchat.send_message(message)

            print "Send card to room %d and Hipchat returned %d" % (self.arguments.room, response_code)
        elif self.arguments.type == "html":
            message = dict(
                color = self.arguments.color,
                message_format = "html",
                message = self.arguments.message
            )
            response_code = self.hipchat.send_message(message)

            print "Send html to room %d and Hipchat returned %d" % (self.arguments.room, response_code)



if __name__ == '__main__':
    HipchatControl()
