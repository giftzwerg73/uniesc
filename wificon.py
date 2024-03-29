import network
import socket
import os
import ure
import time
import config
import ugit

dbgen = 0
def dbgprint(txt):
    if dbgen:
        print(str(txt))


hostnm = config.HOSTNM
ap_ssid = config.APSSID
ap_password = ap_ssid
ap_authmode = config.AP_AUTH

IP = config.IP
SUBNET = config.SUBNET 
GATEWAY = config.GATEWAY
DNS = config.DNS

NETWORK_PROFILES = 'wifi.dat'

network.country(config.COUNTRY)
network.hostname(hostnm)
wlan_ap = network.WLAN(network.AP_IF)
wlan_sta = network.WLAN(network.STA_IF)

wlan_status = None
 
server_socket = None


def get_sta_con(): # return a working WLAN(STA_IF) instance or None
    # First check if there already is any connection:
    if wlan_sta.isconnected():
        return wlan_sta
    
    # Pico connecting to WiFi takes time, wait a bit and try again:
    time.sleep(3)
    if wlan_sta.isconnected():
        return wlan_sta
    
    connected = False    
    # Read known network profiles from file
    profiles = read_profiles()
    if profiles:
        # Search WiFis in range
        wlan_sta.active(True)
        networks = wlan_sta.scan()

        AUTHMODE = {0: "open", 1: "WEP", 2: "WPA-PSK", 3: "WPA2-PSK", 4: "WPA/WPA2-PSK"}
        for ssid, bssid, channel, rssi, authmode, hidden in sorted(networks, key=lambda x: x[3], reverse=True):
            ssid = ssid.decode('utf-8')
            encrypted = authmode > 0
            print("ssid: %s chan: %d rssi: %d authmode: %s" % (ssid, channel, rssi, AUTHMODE.get(authmode, '?')))
            if ssid in profiles:
                if encrypted:
                    password = profiles[ssid]
                    connected = do_connect(ssid, password)
                else:
                    connected = do_connect(ssid, None)
            if connected:
                break
            
    if connected is False:
        # not connected to station
        wlan_sta.active(False)
        return None
    else:
        return wlan_sta


def run_ap(useprofiles):
    # deactivate ap
    wlan_ap.active(False)
    while wlan_ap.active() == True:
        pass
    if useprofiles != 0:
        profiles = read_profiles()
        if ap_ssid in profiles:
            ap_password = profiles[ap_ssid]
    else:
        ap_ssid = "escAP666"
        ap_password = "escAP666"
        hostnm = "escAP666"
    wlan_ap.config(essid=ap_ssid, password=ap_password, hostname=hostnm)
    # activate ap
    wlan_ap.active(True)
    while wlan_ap.active() == False:
        pass
    wlan_ap.ifconfig((IP, SUBNET, GATEWAY, DNS))
    return wlan_ap


def read_profiles():
    profiles = {}
    try:
        with open(NETWORK_PROFILES) as f:
            lines = f.readlines()
        for line in lines:
            ssid, password = line.strip("\n").split(";")
            profiles[ssid] = password
    except OSError as e:
        print("Error Reading Wifi Credentials", str(e))
        profiles = {}
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

def save_profile(ssid, pw):
    profiles = read_profiles()     
    profiles[ssid] = pw
    write_profiles(profiles)
    return True

def del_profile(ssid):
    profiles = read_profiles()     
    dbgprint(profiles)
    if ssid in profiles:
       del profiles[ssid]
       dbgprint(profiles)
       write_profiles(profiles)
       return True
    return False
 
def set_wlan_status(stat):
     global wlan_status
     wlan_status = stat
 
def get_wlan_status():
     global wlan_status
     return wlan_status
    
def get_known_stations():
    try:
        profiles = read_profiles()
    except OSError:
        profiles = {}
    return profiles


# call function in main
def wifi_connect(em):
    if em == 0: # hard coded ap config 
        wlan_ap = run_ap(0)
        print(wlan_ap)
        print(wlan_ap.config("essid"))
        print("APEM up. Network config: ", wlan_ap.ifconfig())
        set_wlan_status(["APEM", wlan_ap])
    else:    
        # try to connect to station
        wlan_sta = get_sta_con()
        if wlan_sta != None:
            # connected to station
            print(wlan_sta)
            print(wlan_sta.config("essid"))
            print("Connected. Network config: ", wlan_sta.ifconfig())
            set_wlan_status(["STA", wlan_sta])
        else: # open ap
            wlan_ap = run_ap(1)
            print(wlan_ap)
            print(wlan_ap.config("essid")) 
            print("AP up. Network config: ", wlan_ap.ifconfig())
            set_wlan_status(["AP", wlan_ap])
    
    