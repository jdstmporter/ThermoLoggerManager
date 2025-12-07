#!/usr/bin/env python3
from web.common import Params
from web.wsgi import WSGIApp

# need to set pythonpath in here, so it includes /usr/local/src/web

params = Params.load('/etc/thermologger/config.json')
application = WSGIApp(params)
