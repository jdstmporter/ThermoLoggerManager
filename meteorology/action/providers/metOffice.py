from meteorology.action.api import BaseMeteorologyProvider, GeographicLocation, BaseMeteorologyData, MeteorologyDatum

class MetOfficeData(BaseMeteorologyData):
    def __init__(self,dat : dict):
        super().__init__(dat)
        try:
            values = self.json.features[0].properties.timeSeries
            self.items = [MeteorologyDatum(values[i].time,
                                           values[i].screenTemperature,
                                           values[i].screenRelativeHumidity) for i in range(len(values))]
        except Exception as e:
            print(f'Error: {e}')
            self.items=[]




class MetOfficeProvider(BaseMeteorologyProvider):
    SPOT_API = 'eyJ4NXQjUzI1NiI6Ik5XVTVZakUxTkRjeVl6a3hZbUl4TkdSaFpqSmpOV1l6T1dGaE9XWXpNMk0yTWpRek5USm1OVEE0TXpOaU9EaG1NVFJqWVdNellXUm1ZalUyTTJJeVpBPT0iLCJraWQiOiJnYXRld2F5X2NlcnRpZmljYXRlX2FsaWFzIiwidHlwIjoiSldUIiwiYWxnIjoiUlMyNTYifQ==.eyJzdWIiOiJqdWxpYW5AcG9ydGVybmV0Lm5ldEBjYXJib24uc3VwZXIiLCJhcHBsaWNhdGlvbiI6eyJvd25lciI6Imp1bGlhbkBwb3J0ZXJuZXQubmV0IiwidGllclF1b3RhVHlwZSI6bnVsbCwidGllciI6IlVubGltaXRlZCIsIm5hbWUiOiJzaXRlX3NwZWNpZmljLTUwYzBhNGFlLTc1ZGUtNGZjZi1hZTQ2LWUxMWUzODZmMDA3MSIsImlkIjo0MzAzNCwidXVpZCI6IjY1YjM5ZDVkLTZjYzktNGU2NS1iZDNiLTA3YTUyYTQyZGY2NiJ9LCJpc3MiOiJodHRwczpcL1wvYXBpLW1hbmFnZXIuYXBpLW1hbmFnZW1lbnQubWV0b2ZmaWNlLmNsb3VkOjQ0M1wvb2F1dGgyXC90b2tlbiIsInRpZXJJbmZvIjp7IndkaF9zaXRlX3NwZWNpZmljX2ZyZWUiOnsidGllclF1b3RhVHlwZSI6InJlcXVlc3RDb3VudCIsImdyYXBoUUxNYXhDb21wbGV4aXR5IjowLCJncmFwaFFMTWF4RGVwdGgiOjAsInN0b3BPblF1b3RhUmVhY2giOnRydWUsInNwaWtlQXJyZXN0TGltaXQiOjAsInNwaWtlQXJyZXN0VW5pdCI6InNlYyJ9fSwia2V5dHlwZSI6IlBST0RVQ1RJT04iLCJzdWJzY3JpYmVkQVBJcyI6W3sic3Vic2NyaWJlclRlbmFudERvbWFpbiI6ImNhcmJvbi5zdXBlciIsIm5hbWUiOiJTaXRlU3BlY2lmaWNGb3JlY2FzdCIsImNvbnRleHQiOiJcL3NpdGVzcGVjaWZpY1wvdjAiLCJwdWJsaXNoZXIiOiJKYWd1YXJfQ0kiLCJ2ZXJzaW9uIjoidjAiLCJzdWJzY3JpcHRpb25UaWVyIjoid2RoX3NpdGVfc3BlY2lmaWNfZnJlZSJ9XSwidG9rZW5fdHlwZSI6ImFwaUtleSIsImlhdCI6MTc3NDM2OTg4MSwianRpIjoiYmE4ZGY0NzQtZTIzMC00MjMxLWJhMzgtOGM0ZDkxMzMxNmU3In0=.fcCZWTbFFNirk9a_2j83QEN6kWlfixDdP5HBvlDejEmE2MvqOGG1i6mXzYsOhW32WUSajs38sn7ZTDHhypTpxc1edFUQWeBfW_HIZFsi6anMzZfYeuRFGXqdB9Mv8R9nfs9CRXSTCD-7tCj6obWWeEL4-FwoK_rFBC3i5EX9_wFSaAbCWtP_b9-Ndu5knzLQemuvbemSObJn44YfALaJXIAoV2v1uslTVMVQjs2ggIagJmG9I6Oah7CnMEJ4DGPz9pXzUDaIsWxFSHmlnqG0W4XoX7MtDX_zQJbUcG3Ph6KOSzNjiaSIVx26Wa211DldE16xdg0w3Q_7Z2bFZAg32w=='
    URL = 'https://data.hub.api.metoffice.gov.uk/sitespecific/v0/point/hourly'

    def __init__(self, centre: GeographicLocation,path : str, apikey : str):
        super().__init__(centre, path, apikey)



    def attributes(self):
        return dict(
            datasource='BD1',
            includeLocationName='true',
            latitude=str(self.centre.latitude),
            longitude=str(self.centre.longitude)
        )

    def headers(self):
        return dict(apikey=self.apikey)

    @classmethod
    def dataStructure(cls,json):
        return MetOfficeData(json)


