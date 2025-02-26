import mysql.connector

from processor.thingspeak import ThingSpeakRecord



class SQLStore:

    def __init__(self,params):
        self.db = mysql.connector.connect(database=params.db_database,host=params.db_host,user=params.db_user,password=params.db_password)

    def close(self):
        self.db.close()

    def read(self) -> [ThingSpeakRecord]:
        cursor = self.db.cursor()
        query = 'select seq, timestamp, temperature, humidity, battery, sensor FROM records ORDER BY seq'
        cursor.execute(query)
        out = []
        for (seq, timestamp, temperature, humidity, battery, sensor) in cursor:
            item = dict(
                entry_id=seq,
                field2=sensor,
                field3=temperature,
                field4=humidity,
                field5=battery,
                field7=timestamp
            )
            out.append(ThingSpeakRecord(item))
        cursor.close()
        return out

    def _get_pks(self) -> set :
        cursor = self.db.cursor()
        cursor.execute('select seq FROM records')
        seqs = { x[0] for x in cursor }
        cursor.close()
        return seqs


    def write(self,records : [ThingSpeakRecord]):
        existing = self._get_pks()
        vals = ', '.join([r.sql() for r in records if r.sequence not in existing])
        sql = f"INSERT INTO records (seq, timestamp, temperature, humidity, battery, sensor) values {vals}"
        print(sql)
        cursor = self.db.cursor()
        cursor.execute(sql)
        self.db.commit()
        cursor.close()


