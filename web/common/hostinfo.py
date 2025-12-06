import platform
import re

class _HostInfo:
    def __init__(self):
        self.system = platform.system()
        self.architecture = platform.machine()
        self.release = platform.release()

        self.rpi = re.search('rpi',self.release) is not None

    @property
    def is_MAC(self):
        return self.system=='Darwin'

    @property
    def is_linux(self):
        return self.system=='Linux'

    @property
    def is_windows(self):
        return self.system=='Windows'

    @property
    def is_RPI(self):
        return self.is_linux and self.architecture=='aarch64' and self.rpi

    @property
    def is_Server(self):
        return self.is_linux and not self.rpi


HostInfo = _HostInfo()