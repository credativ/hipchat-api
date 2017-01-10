# hipchat-api
This repository contains a small HipChat API written in Python. It allows you to send text, html and card messages to a given HipChat room.

## Installation
If you want to install this package, simply type in the following command within the cloned directory:
```
sudo python setup.py install
```

The output should like like this:
```
running install
running build
running build_py
copying src/hipchat/api.py -> build/lib.linux-x86_64-2.7/hipchat
running install_lib
copying build/lib.linux-x86_64-2.7/hipchat/api.py -> /usr/local/lib/python2.7/dist-packages/hipchat
byte-compiling /usr/local/lib/python2.7/dist-packages/hipchat/api.py to api.pyc
running install_egg_info
Removing /usr/local/lib/python2.7/dist-packages/hipchat_api-1.0.egg-info
Writing /usr/local/lib/python2.7/dist-packages/hipchat_api-1.0.egg-info
```

Now you are able to import this module by adding the following line to your script:
```
from hipchat.api import HipchatAPI
```

## Configuration
The HipchatAPI class uses a given .ini file to obtain all information it needs to connect to a corresponding Hipchat room.
The following example should how the configuration file should look like:
```
[hipchat]                                                                                                                                                                                                                                     
url = https://<URL>
token = <ACCESS TOKEN>
room = <Room ID>
timeout = <Timeout in seconds>
```

## Usage
You can find a simple script called hipchatctl.py in this repository. 
This little tool shows how it uses the methods of the HipchatAPI class to write message or cards.

Take a look into it to learn more about the methods and how to use them.
