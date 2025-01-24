import bleak
import asyncio

from ..data import AdvertisingResponse, ThermoBeaconValues

class ScanForUpdates:
    def __init__(self, params):
        self.timeout = params.scan_time
        self.response_length = params.response_length
        self.name = params.name
        self.macs = []
        self.beacons = []

    def check(self, response):
        if response.name_is(self.name) :
            return response.mac not in self.macs
        else:
            return False

    def action(self, response):
        received = []
        for k, v in response:
            if len(v) == self.response_length:
                received.append(ThermoBeaconValues(k, v))
        if len(received)>0:
            rcv = received[0]
            self.macs.append(response.mac)
            self.beacons.append(rcv)
            print(f'Found {response.name}@{rcv.id}: [{response.mac}] {rcv.hex()}')

    def callback(self, device : bleak.BLEDevice, ad_data : bleak.AdvertisementData):
        response = AdvertisingResponse(device,ad_data)
        if self.check(response):
            self.action(response)

    async def __call__(self):
        scanner = bleak.BleakScanner(self.callback)
        await scanner.start()
        await asyncio.sleep(self.timeout)
        await scanner.stop()

    def run(self) -> [ThermoBeaconValues] :
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self())
            return self.beacons
        except KeyboardInterrupt:
            print()
            return []
