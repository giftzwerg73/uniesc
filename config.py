import machine

# try machine dependant initialisation
try:
    _chip_id = machine.mem32[0x40000000]
    _rev = (_chip_id >> 28) & 0x0F
    _part = (_chip_id >> 12) & 0xFFFF
    _model = "1" if _part == 0x0002 else "2" if _part in (0x0003, 0x0004) else "X"
    HWREF = "{}.{:X}".format(_model, _rev)
except Exception:
    HWREF = "0.0"

try:
    _uid = machine.unique_id()
    SERIAL = "{:06d}".format(int.from_bytes(_uid, 'big') % 1000000)
except (ImportError, Exception):
    SERIAL = "000001"


# user editable config
# wifi stuff
APSSID = "escAP-" + SERIAL[2:6]
HOSTNM = "uniesc-" + SERIAL[2:6]
IP = "192.168.4.1"
SUBNET = "255.255.255.0"
GATEWAY = "192.168.4.1"
DNS = "192.168.4.1"
AP_AUTH = 4  # WPA/WPA2
COUNTRY = "XX"
