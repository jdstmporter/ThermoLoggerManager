
from thermologger.api import ScanForUpdates
from .mysql_records import SensorSQLStore
from thermologger.common import syslog, LogLevel


class Action:

    def __init__(self,params):
        self.scanner = ScanForUpdates(params)
        self.db = SensorSQLStore(params)

    def __call__(self):
        beacons = self.scanner.run()

        if syslog.isDebug:
            syslog(LogLevel.DEBUG, f'Got {len(beacons)} records')
            for beacon in beacons:
                syslog(LogLevel.DEBUG, str(beacon))

        if len(beacons) > 0:
            records = [b.record() for b in beacons]
            syslog(LogLevel.INFO, 'Contacting SQL')
            try:
                self.db.write_records(records)
                syslog(LogLevel.INFO, 'Uploaded')
            except Exception as e:
                syslog(LogLevel.ERROR, f'Error: {str(e)}')