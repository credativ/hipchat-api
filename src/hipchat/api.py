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
