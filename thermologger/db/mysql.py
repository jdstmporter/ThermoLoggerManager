import math

import mysql.connector
from thermologger.common import LogLevel, syslog
from thermologger.common.records import Record
from datetime import datetime


class SQLStore:

    def __init__(self,params):
        print(f'Connecting to mysql')
        database = params.db_database
        host = params.db_host
        user = params.db_user
        password = params.db_password
        port = params.db_port
        print(f'DB = {database} HOST = {host} USER = {user} PASSWORD = {password} PORT = {port}')
        self.db = mysql.connector.connect(database=database,host=host,
                                          user=user,password=password,
                                          port=port)

    def close(self):
        self.db.close()

    def check(self):
        if not self.db.is_connected():
            syslog(LogLevel.INFO,'MySQL connection stale; attempting to reconnect')
            self.db.reconnect()


    def _query(self,sql) -> list[tuple]:
        self.check()
        cursor = self.db.cursor()
        cursor.execute(sql)
        out = cursor.fetchall()
        cursor.close()
        return out

    def _write(self,sql):
        self.check()
        cursor = self.db.cursor()
        cursor.execute(sql)
        self.db.commit()
        cursor.close()


    def time_range(self):
        out = self._query('select min(timestamp), max(timestamp) from records')
        if len(out)>0:
            return TimeInterval(*out[0])
        else:
            return TimeInterval(end=int(datetime.now().timestamp()))


    def read(self,range=None) -> list[Record]:
        if range is None:
            q='SELECT mac, sensor, timestamp, temperature, humidity, battery FROM records ORDER BY seq'
        else:
            q=f'SELECT mac, sensor, timestamp, temperature, humidity, battery FROM records WHERE timestamp>{range.start} AND timestamp<{range.end} ORDER BY seq'

        rows = self._query(q)
        out = []
        for (mac, sensor, timestamp, temperature, humidity, battery) in rows:
            out.append(Record(mac, sensor, temperature, humidity, battery, timestamp))
        return out



    def beacons(self) -> dict:
        try:
            rows = self._query('SELECT mac, name from sensors')
            out = {mac: name for (mac, name) in rows}
        except Exception as e:
            syslog(LogLevel.ERROR,f'Error loading beacons list: {e}')
            out = {}

        return out

    def _get_pks(self) -> set :
        out = self._query('select seq FROM records')
        seqs = { x[0] for x in out }
        return seqs

    def next_pk(self):
        cursor = self.db.cursor()
        cursor.execute('select max(seq) FROM records')
        record = cursor.fetchone()
        return record[0]+1


    def write(self,records : list[Record]):
        beacons = self.beacons()
        vals = ', '.join([r.sql(beacons) for r in records])
        sql = f"INSERT INTO records (mac, sensor, timestamp, temperature, humidity, battery) values {vals}"
        print(sql)
        self.check()
        cursor = self.db.cursor()
        cursor.execute(sql)
        self.db.commit()
        cursor.close()








