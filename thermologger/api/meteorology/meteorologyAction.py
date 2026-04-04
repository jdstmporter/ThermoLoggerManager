from .api import GeographicLocation, BaseMeteorologyProvider
from .mysql_meteorology import MeteorologySQLStore
from thermologger.common import LogLevel, syslog

class MeteorologyAction:
    def __init__(self,params):
        p = params.meteo
        centre=GeographicLocation(p.latitude, p.longitude)
        self.provider = BaseMeteorologyProvider.Load(p.provider)(centre, p.path, p.apiKey)
        self.sql = MeteorologySQLStore(params)

    def __call__(self):
        try:
            data = self.provider()
            for item in data:
                print(str(item))
            self.sql.insert_meteorologyData(data)
        except Exception as e:
            syslog(LogLevel.ERROR, f'Error: {str(e)}')


