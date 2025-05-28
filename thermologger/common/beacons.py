

MACS = {
    "c21200008b9d": 'Choir',
    "dc060000f29d": 'Kitchen',
    "fc0200008b9d": 'Organ',
    "690600008b9d": 'Pulpit',
    "ab0100008b9d": 'Lady Chapel',
    "260b0000f29d": 'TEST'
}

class Beacon:

    def __init__(self,mac : str,name : str | None = None,known : bool = True):
        self.mac =mac
        self.name = name
        self.known = known

    def json(self) :
        return {
            'mac' : self.mac,
            'name' : self.name,
            'known' : self.known
        }

    def sql(self):
        n = self.name if self.name is not None else self.mac
        k = {True: 1, False: 0}[self.known]
        return f"('{self.mac}', '{n}', k)"



class Beacons:

    def __init__(self,beacons : list[Beacon]):
        self.lookup : dict[str,Beacon] = { b.mac : b for b in beacons}
        self.beacons : list[Beacon] = beacons

    def __getitem__(self,mac : str) -> Beacon :
        if mac in self.lookup:
            return self.lookup[mac]
        else:
            return Beacon(mac,mac,False)

    def __iter__(self):
        return iter(self.beacons)

    def __contains__(self, item):
        return item in self.lookup

    def name(self,mac):
        if mac in self.lookup:
            return self.lookup[mac].name
        else:
            return mac

    def isKnown(self,known : bool) -> list[Beacon] :
        return [b for b in self.beacons if b.known==known]

    @property
    def known(self):
        return self.isKnown(True)

    def unknown(self):
        return self.isKnown(False)

    def json(self):
        return [b.json() for b in self.beacons]

    @classmethod
    def fromDB(cls,records : list[tuple[str, str | None, bool | int]]):
        b = [Beacon(m, n, bool(k)) for (m,n,k) in records]
        return Beacons(b)






