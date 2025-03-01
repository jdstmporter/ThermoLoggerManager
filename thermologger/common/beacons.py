MACS = {
    "c21200008b9d": 'Choir',
    "dc060000f29d": 'Kitchen',
    "fc0200008b9d": 'Organ',
    "690600008b9d": 'Pulpit',
    "ab0100008b9d": 'Lady Chapel',
    "260b0000f29d": 'TEST'
}

def beacon(mac):
    if mac in MACS:
        return MACS[mac]
    else:
        return mac