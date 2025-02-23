import datetime


def decode_temperature(b:bytes) -> float:
    result = int.from_bytes(b, byteorder='little')/16.0
    if result>4000:
        result -= 4096
    return result

'''
decode humidity value from byte(2) array
'''

def decode_humidity(b:bytes) -> float:
    result = int.from_bytes(b, byteorder='little')/16.0
    if result>4000:
        result -= 4096
    return result

class ThermoBeaconValues:
    def __init__(self,key: int, value: bytes):
        self.id = key
        self.raw = value

        self.button = False if value[1] == 0 else True
        self.mac = value[2:8].hex()
        battery = int.from_bytes(value[8:10], byteorder='little')
        self.battery = battery * 100 / 3400
        self.temperature = decode_temperature(value[10:12])
        self.humidity = decode_humidity(value[12:14])
        self.uptime = int.from_bytes(value[14:18], byteorder='little')

    def hex(self):
        return self.raw.hex()

    def __str__(self):
        return '\n'.join([f'MAC = [{self.mac}] ID = {self.id}',
                          f'Temperature = {self.temperature}',
                          f'Humidity = {self.humidity}',
                          f'Battery = {self.battery}',
                          f'Uptime = {self.uptime}'])

    def dict(self,offset=0):
        now = datetime.datetime.now() + datetime.timedelta(seconds=offset)
        return dict(
            created_at = now.strftime('%Y-%m-%d %H:%M:%S %z'),
            field1 = "ThermoBeacon",
            field2 = str(self.mac),
            field3 = str(self.temperature),
            field4 = str(self.humidity),
            field5 = str(self.battery),
            field6 = str(self.uptime),
            field7 = str(now.timestamp())
        )