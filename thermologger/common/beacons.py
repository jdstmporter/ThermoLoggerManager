

MACS = {
    "c21200008b9d": 'Choir',
    "dc060000f29d": 'Kitchen',
    "fc0200008b9d": 'Organ',
    "690600008b9d": 'Pulpit',
    "ab0100008b9d": 'Lady Chapel',
    "260b0000f29d": 'TEST',
    "610400008c6c": 'NEW 1',
    "880400008c6c": 'NEW 2'
}

class Beacons:

    def __init__(self,raw={}):
        self.beacons=raw

    def __getitem__(self,mac):
        return self.beacons.get(mac,mac)






