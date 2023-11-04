import network
import socket
import ure
import time
from debug import dbgprint

ap_ssid = "ESCProg"
ap_password = "ESCProg123"
ap_authmode = 3  # WPA2
hostnm = "escprog"

IP =      "192.168.4.1"
SUBNET =  "255.255.255.0"
GATEWAY = "192.168.4.1"
DNS =     "0.0.0.0"

NETWORK_PROFILES = 'wifi.dat'

network.country('DE')
network.hostname(hostnm)
wlan_ap = network.WLAN(network.AP_IF)
wlan_sta = network.WLAN(network.STA_IF)

server_socket = None


def get_sta_con(): # return a working WLAN(STA_IF) instance or None
    # First check if there already is any connection:
    if wlan_sta.isconnected():
        return wlan_sta

    connected = False
    try:
        # Pico connecting to WiFi takes time, wait a bit and try again:
        time.sleep(3)
        if wlan_sta.isconnected():
            return wlan_sta

        # Read known network profiles from file
        profiles = read_profiles()

        # Search WiFis in range
        wlan_sta.active(True)
        networks = wlan_sta.scan()

        AUTHMODE = {0: "open", 1: "WEP", 2: "WPA-PSK", 3: "WPA2-PSK", 4: "WPA/WPA2-PSK"}
        for ssid, bssid, channel, rssi, authmode, hidden in sorted(networks, key=lambda x: x[3], reverse=True):
            ssid = ssid.decode('utf-8')
            encrypted = authmode > 0
            print("ssid: %s chan: %d rssi: %d authmode: %s" % (ssid, channel, rssi, AUTHMODE.get(authmode, '?')))
            if encrypted:
                if ssid in profiles:
                    password = profiles[ssid]
                    connected = do_connect(ssid, password)
                else:
                    print("skipping unknown encrypted network")
            else:  # open
                connected = do_connect(ssid, None)
            if connected:
                break

    except OSError as e:
        print("exception", str(e))
    
    if connected is False:
        # not connected to station
        wlan_sta.active(False)
        while wlan_sta.active() == True:
            pass
        return None
    else:
        return wlan_sta


def run_ap():
    wlan_ap.active(False)
    while wlan_ap.active() is True:
        pass
    wlan_ap.config(essid=ap_ssid, password=ap_password, hostname=hostnm)
    wlan_ap.active(True)
    while wlan_ap.active() is False:
        pass
    wlan_ap.ifconfig((IP, SUBNET, GATEWAY, DNS))
    return wlan_ap


def read_profiles():
    with open(NETWORK_PROFILES) as f:
        lines = f.readlines()
    profiles = {}
    for line in lines:
        ssid, password = line.strip("\n").split(";")
        profiles[ssid] = password
    return profiles


def write_profiles(profiles):
    lines = []
    for ssid, password in profiles.items():
        lines.append("%s;%s\n" % (ssid, password))
    with open(NETWORK_PROFILES, "w") as f:
        f.write(''.join(lines))


def do_connect(ssid, password):
    wlan_sta.active(True)
    if wlan_sta.isconnected():
        return None
    print('Trying to connect to %s...' % ssid)
    wlan_sta.connect(ssid, password)
    for retry in range(100):
        connected = wlan_sta.isconnected()
        if connected:
            break
        time.sleep(0.1)
        print('.', end='')
    if connected:
        #print('\nConnected. Network config: ', wlan_sta.ifconfig())
        pass
    else:
        print('\nFailed. Not Connected to: ' + ssid)
    return connected

            
def scan4ap():
    wlan_sta.active(True)
    ssids = sorted(ssid.decode('utf-8') for ssid, *_ in wlan_sta.scan())
    return ssids


def connectnsave(ssid, password):
    con = do_connect(ssid, password)
    if con == None:
        dbgprint("Already connected")
    elif con == True:
        try:
            profiles = read_profiles()
        except OSError:
            profiles = {}
        
        profiles[ssid] = password
        write_profiles(profiles)
        time.sleep(5)
        return True
    else:
        dbgprint("Connection failed")
        return False
    