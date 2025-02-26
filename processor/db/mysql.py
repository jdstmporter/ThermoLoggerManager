import mysql.connector

from processor.thingspeak import Record



class SQLStore:

    def __init__(self,params):
        self.db = mysql.connector.connect(database=params.db_database,host=params.db_host,user=params.db_user,password=params.db_password)

    def close(self):
        self.db.close()

    def read(self) -> [Record]:
        cursor = self.db.cursor()
        query = 'select timestamp, temperature, humidity, battery, sensor FROM records ORDER BY seq'
        cursor.execute(query)
        out = []
        for (timestamp, temperature, humidity, battery, sensor) in cursor:
            out.append(Record(timestamp, temperature, humidity, battery, sensor))
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
        vals = ', '.join([r.sql() for r in records])
        sql = f"INSERT INTO records (timestamp, temperature, humidity, battery, sensor) values {vals}"
        print(sql)
        cursor = self.db.cursor()
        cursor.execute(sql)
        self.db.commit()
        cursor.close()


