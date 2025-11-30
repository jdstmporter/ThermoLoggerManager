import mysql.connector

from thermologger.common import LogLevel, syslog
from thermologger.common.records import Record
from datetime import datetime


class SQLStore:

    def __init__(self,params):
        print(f'Connecting to mysql')
        print(f'DB = {params.db_database} HOST = {params.db_host} USER = {params.db_user} PASSWORD = {params.db_password} PORT = {params.db_port}')
        self.db = mysql.connector.connect(database=params.db_database,host=params.db_host,
                                          user=params.db_user,password=params.db_password,
                                          port=params.db_port)

    def close(self):
        self.db.close()

    def check(self):
        if not self.db.is_connected():
            syslog(LogLevel.INFO,'MySQL connection stale; attempting to reconnect');
            self.db.reconnect()

    def _query(self,sql) -> list[tuple]:
        self.check()
        cursor = self.db.cursor()
        cursor.execute(sql)
        out = [x for x in cursor]
        cursor.close()
        return out

    def time_range(self):
        out = self._query('select max(timestamp), min(timestamp) from records')
        if len(out)>0:
            return out[0]
        else:
            return (datetime.now().timestamp(),0)


    def read(self) -> [Record]:
        self.check()
        cursor = self.db.cursor()
        query = 'SELECT mac, sensor, timestamp, temperature, humidity, battery FROM records ORDER BY seq'
        cursor.execute(query)
        out = []
        for (mac, sensor, timestamp, temperature, humidity, battery) in cursor:
            out.append(Record(mac, sensor, temperature, humidity, battery, timestamp))
        cursor.close()
        return out

    def beacons(self) -> dict:
        try:
            self.check()
            cursor = self.db.cursor()
            query = 'SELECT mac, name from sensors'
            cursor.execute(query)
            out = {mac: name for (mac, name) in cursor}
            cursor.close()
        except:
            out = {}

        return out

    def _get_pks(self) -> set :
        cursor = self.db.cursor()
        cursor.execute('select seq FROM records')
        seqs = { x[0] for x in cursor }
        cursor.close()
        return seqs

    def next_pk(self):
        cursor = self.db.cursor()
        cursor.execute('select max(seq) FROM records')
        record = cursor.fetchone()
        return record[0]+1


    def write(self,records : [Record]):
        beacons = self.beacons()
        vals = ', '.join([r.sql(beacons) for r in records])
        sql = f"INSERT INTO records (mac, sensor, timestamp, temperature, humidity, battery) values {vals}"
        print(sql)
        self.check()
        cursor = self.db.cursor()
        cursor.execute(sql)
        self.db.commit()
        cursor.close()




