import bleak

class AdvertisingResponse:
    def __init__(self, device : bleak.BLEDevice, advert : bleak.AdvertisementData):
        self.mac = device.address.lower()
        self.device_name = device.name
        self.name = advert.local_name
        self.details = device.details
        self.data = advert.manufacturer_data
        self.rssi = advert.rssi
        self.tx_power = advert.tx_power

    def __iter__(self):
        for k, v in self.data.items():
            yield k, v

    def __getitem__(self, key):
        return self.data[key]

    def __contains__(self, item):
        return item in self.data.keys()

    def __str__(self):
        return f'[{self.mac}] {self.name}({self.device_name}) {self.rssi}'

    def name_is(self, name: str):
        return self.name is not None and self.name == name