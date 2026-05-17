from thermologger.db import SQLStore
from .api import MeteorologyDatum

class MeteorologySQLStore(SQLStore):

    def insert_meteorologyData(self,data):
        vals = ', '.join([r.sql() for r in data])
        sql = f"REPLACE INTO meteorology (timestamp, temperature, humidity) values {vals}"
        print(sql)
        self._write(sql)

    def read_meteorologyData(self,range=None):
        if range is None:
            q = 'SELECT timestamp, temperature, humidity FROM meteorology ORDER BY timestamp'
        else:
            q = f'SELECT timestamp, temperature, humidity FROM meteorology WHERE timestamp>{range.start} AND timestamp<{range.end} ORDER BY timestamp'

        rows = self._query(q)
        out = []
        for (timestamp, temperature, humidity) in rows:
            out.append(MeteorologyDatum(temperature, humidity, timestamp))
        return out


