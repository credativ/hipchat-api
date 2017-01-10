# -------------------------------------------------------------------------------- #
# Copyright (c) 2017 Michael Sprengel for credativ GmbH
# www.credativ.de
#
# powered by Swisscom Health AG | www.swisscom.com/health
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
# Important includes
#
import os
import json
import requests
import ConfigParser


#
# This class adds an abstraction layer for the
# Hipchat API v2
#
class HipchatAPI(object):

    #----------------------------------------
    def __init__(self, config_file = None, url = None, token = None, room = None, timeout = None):
    #----------------------------------------
        # Initialize variable
        self.url = url
        self.token = token
        self.room = room
        self.timeout = timeout

        # Load settings
        self.load_settings(config_file)

        # Verify settings
        assert (self.url is not None), "There is no URL configured within HipChat's configuration."
        assert (self.token is not None), "No token has been specified within HipChat's configuration."
        assert (self.room is not None), "No room has been specified within HipChat's configuration."

    #----------------------------------------
    def load_settings(self, config_file):
    #----------------------------------------
        if config_file is None:
            return

        if not os.path.isfile(config_file):
            raise Exception('\nCould not find configuration file %s' % config_file)

        config = ConfigParser.ConfigParser()
        config.read(config_file)

        if self.url is None:
            self.url = config.get('hipchat', 'url')
        if self.token is None:
            self.token = config.get('hipchat', 'token')
        if self.room is None:
            self.room = config.get('hipchat', 'room')
        if self.timeout is None:
            self.timeout = int(config.get('hipchat', 'timeout'))

    #----------------------------------------
    def send_message(self, data):
    #----------------------------------------
        data_string = json.dumps(data, indent=4, ensure_ascii=True)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % self.token
        }

        # Send HTTP request
        response = requests.post(
            url = "%s/v2/room/%s/notification" % (self.url, self.room),
            data = data_string,
            headers = headers,
            timeout = self.timeout
        )

        # Interpret response
        return response.status_code
