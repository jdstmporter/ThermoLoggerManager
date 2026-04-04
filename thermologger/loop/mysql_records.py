from thermologger.db import SQLStore
from thermologger.common import LogLevel, syslog, Record
from datetime import datetime

class TimeInterval:
    def __init__(self,start = 0,end = 0xffffffff):
        if start<end:
            self.start=start
            self.end=end
        else:
            self.start = start
            self.end = start
            self.end = start

    def intersect(self,other):
        start = max(self.start, other.start)
        end = min(self.end, other.end)
        return TimeInterval(start,end)

    def __call__(self):
        return (self.start,self.end)


class SensorSQLStore(SQLStore):

    def read_time_range(self):
        out = self._query('select min(timestamp), max(timestamp) from records')
        if len(out) > 0:
            return TimeInterval(*out[0])
        else:
            return TimeInterval(end=int(datetime.now().timestamp()))

    def read_records(self, range=None) -> list[Record]:
        if range is None:
            q = 'SELECT mac, sensor, timestamp, temperature, humidity, battery FROM records ORDER BY seq'
        else:
            q = f'SELECT mac, sensor, timestamp, temperature, humidity, battery FROM records WHERE timestamp>{range.start} AND timestamp<{range.end} ORDER BY seq'

        rows = self._query(q)
        out = []
        for (mac, sensor, timestamp, temperature, humidity, battery) in rows:
            out.append(Record(mac, sensor, temperature, humidity, battery, timestamp))
        return out

    def write_records(self, records: list[Record]):
        beacons = self.beacons()
        vals = ', '.join([r.sql(beacons) for r in records])
        sql = f"INSERT INTO records (mac, sensor, timestamp, temperature, humidity, battery) values {vals}"
        print(sql)
        self.check()
        cursor = self.db.cursor()
        cursor.execute(sql)
        self.db.commit()
        cursor.close()

    def _get_record_pks(self) -> set:
        out = self._query('select seq FROM records')
        seqs = {x[0] for x in out}
        return seqs

    def next_record_pk(self):
        cursor = self.db.cursor()
        cursor.execute('select max(seq) FROM records')
        record = cursor.fetchone()
        return record[0] + 1

    def read_beacons(self) -> dict:
        try:
            rows = self._query('SELECT mac, name from sensors')
            out = {mac: name for (mac, name) in rows}
        except Exception as e:
            syslog(LogLevel.ERROR, f'Error loading beacons list: {e}')
            out = {}
        return out
