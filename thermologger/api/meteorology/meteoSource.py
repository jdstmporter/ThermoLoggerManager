from .api import BaseMeteorologyProvider, BaseMeteorologyData, GeographicLocation, MeteorologyDatum


class MeteoSourceData(BaseMeteorologyData):
    def __init__(self,dat : dict):
        super().__init__(dat)
        try:
            values=self.json.hourly.data
            self.items = [MeteorologyDatum(f'{values[i].date}Z',
                                           values[i].temperature,
                                           None) for i in range(len(values))]
        except Exception as e:
            print(f'Error: {e}')
            self.items=[]



class MeteoSourceProvider(BaseMeteorologyProvider):

    def __init__(self, centre: GeographicLocation):
        super().__init__(centre)

    def url(self):
        return 'https://www.meteosource.com/api/v1/free/point'

    def attributes(self):
        return dict(
            lat = self.centre.latitudeNS,
            lon = self.centre.longitudeEW,
            sections = 'current,hourly',
            timezone = 'UTC',
            language = 'en',
            units = 'metric'
        )

    def headers(self):
        return {
            'X-API-Key' : '7s98p82l8fvqiaj7ct4nkbq7zpj2565iikzr5qht',
            'accept' : 'application/json'
        }


def runMeteoSource():
    try:
        r=MeteoSourceProvider(GeographicLocation(51.90006, -2.07972))
        json=r()
        print(str(json))
        data = MeteoSourceData(json)
        for item in data:
            print(str(item))
    except Exception as e:
        print(str(e))