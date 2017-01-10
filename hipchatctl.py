#!/usr/bin/env python
# -------------------------------------------------------------------------------- #
# Copyright (c) 2017 Michael Sprengel for credativ GmbH
# www.credativ.de
#
# powered by Swisscom Health AG | www.swisscom.com/health
#
# Copyright (c) 2017 Michael Sprengel
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
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
