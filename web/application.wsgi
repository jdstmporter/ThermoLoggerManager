#!/usr/bin/env python3

from pathlib import Path
import sys
root_dir = Path(__file__).parent.absolute()
sys.path.append(str(root_dir))
print(f'PYTHONPATH={":".join(sys.path)}')

from web.wsgi import WSGIApplication

application = WSGIApplication('/etc/thermologger/config.json')()