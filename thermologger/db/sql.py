import enum
import math
from typing import cast

from .mysql import SQLStore
from ..common import Record
from ..common.beacons import Beacons, Beacon


class TimeRange:
    def __init__(self,data: list[tuple[float,float]] ):
        if len(data)>0:
            self.max = data[0][0]
            self.min = data[0][1]
        else:
            self.max = 0xffffffff
            self.min = 0


    def json(self):
        return { 'max' : self.max, 'min' : self.min }

class Actions(enum.Enum):
    ReadBeacons = 1
    WriteBeacons = 2
    ReadRecords = 3
    WriteRecords = 4
    ReadTimeRange = 5


    def query(self,records : list[Record]=[], beacons : list[Beacon]=[]) -> str:
        if self == Actions.ReadBeacons:
            return 'SELECT mac, name, known from sensors'
        elif self == Actions.ReadRecords:
            return 'SELECT mac, sensor, timestamp, temperature, humidity, battery FROM records ORDER BY seq'
        elif self == Actions.ReadTimeRange:
            return 'select max(timestamp), min(timestamp) from records'
        elif self == Actions.WriteBeacons:
            v = ', '.join([b.sql() for b in beacons])
            return "INSERT INTO beacons (mac, name, known) values {v}"
        elif self == Actions.WriteRecords:
            v = ', '.join([r.sql(beacons) for r in records])
            return  f"INSERT INTO records (mac, sensor, timestamp, temperature, humidity, battery) values {v}"
        else:
            return ''



class SQL:

    def __init__(self, params):
        self.sql = SQLStore(params)

    def get(self, action : Actions):
        query = action.query()
        out = self.sql.query(query)

        if action == Actions.ReadBeacons:
            o = cast(list[tuple[str, str | None, bool | int]], out)
            return Beacons.fromDB(o)
        elif action == Actions.ReadRecords:
            return [Record(*x) for x in out]
        elif action == Actions.ReadTimeRange:
            o = cast(list[tuple[float,float]], out)
            return TimeRange(o)
        else:
            return None

    def set(self, action : Actions, records : list[Record]=[], beacons : list[Beacon]=[]):
        if action == Actions.WriteBeacons or action == Actions.WriteRecords:
            query = action.query(records, beacons)
            self.sql.update(query)
