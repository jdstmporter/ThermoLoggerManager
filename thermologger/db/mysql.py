import mysql.connector

from thermologger.common.records import Record
from thermologger.common.beacons import Beacons



class SQLStore:

    def __init__(self,params):
        self.db = mysql.connector.connect(database=params.db_database,host=params.db_host,
                                          user=params.db_user,password=params.db_password,
                                          port=params.db_port)

    def close(self):
        self.db.close()

    def read(self) -> [Record]:
        cursor = self.db.cursor()
        query = 'SELECT mac, sensor, timestamp, temperature, humidity, battery FROM records ORDER BY seq'
        cursor.execute(query)
        out = []
        for (mac, sensor, timestamp, temperature, humidity, battery) in cursor:
            out.append(Record(mac, sensor, temperature, humidity, battery, timestamp))
        cursor.close()
        return out

    def beacons(self) -> dict:
        cursor = self.db.cursor()
        try:
            query = 'SELECT mac, name from sensors'
            cursor.execute(query)
            out = {mac: name for (mac, name) in cursor}
        except:
            out = {}
        cursor.close()
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
        cursor = self.db.cursor()
        cursor.execute(sql)
        self.db.commit()
        cursor.close()




