from .things import ThingSpeakDownloader, ThingSpeakRecord



class MysqlStore:

    def __init__(self,database='picam',host='127.0.0.1',user='sql',password='sql'):
        self.db = MySQLdb.connect(database=database,host=host,user=user,password=password)
        self.cursor = self.db.cursor()

    def close(self):
        self.cursor.close()

    @property
    def cameras(self):

        self.cursor.execute('select model FROM cameras ORDER BY idx')
        items = self.cursor.fetchall()
        return [item[0] for item in items]


    def setCameras(self,cams):
        vals = ", ".join([f"({idx}, '{cams[idx]}')" for idx in range(len(cams))])

        sql = f"INSERT INTO picam.cameras (idx, model) values {vals}"
        print(sql)
        self.cursor.execute('delete from cameras where idx>=0')
        self.cursor.execute(sql)



    @property
    def modes(self):
        self.cursor.execute('select camera, model, format, width, height, fps from modes join cameras on camera=idx')
        raw = self.cursor.fetchall()
        items = [PiCamInfo.fromTuple(row) for row in raw]
        return items


    def setModes(self,modes):
        vals = ", ".join([modeMap(mode) for mode  in modes])
        sql = f"INSERT INTO picam.modes (camera, format, width, height, fps) values {vals}"
        print(sql)
        self.cursor.execute('delete from modes where camera>=0')
        self.cursor.execute(sql)

