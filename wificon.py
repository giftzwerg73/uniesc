import network
import time
import config

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
    global ap_ssid, ap_password, hostnm
    
    # 1. Deactivate AP completely to clear old state
    wlan_ap.active(False)
    while wlan_ap.active():
        time.sleep_ms(1)

    # Set default credentials
    ap_ssid = "escAP-DEFAULT"
    ap_password = "12345678"
    hostnm = "escap.net"
    
    # Check credentials for user ap available, if not fallback
    if useprofiles != 0: 
        profiles = read_profiles()
        if config.APSSID in profiles:
            saved_pw = profiles[config.APSSID]
            if saved_pw and config.HOSTNM:
                ap_ssid = config.APSSID
                ap_password = saved_pw
                hostnm = config.HOSTNM + ".net" 
    
    print(f"SSID: {ap_ssid} PW: {ap_password} HN: {hostnm} DNS:{DNS} SEC: {ap_authmode}")
    # 2. Apply the base SSID and password details
    network.hostname(hostnm)
    wlan_ap.config(essid=ap_ssid, password=ap_password)
    # 3. ACTIVATE THE AP INTERFACE
    wlan_ap.active(True)
    while not wlan_ap.active():
        time.sleep_ms(1)
    # 4. Bind the static IP rules last
    wlan_ap.ifconfig((IP, SUBNET, GATEWAY, DNS))
    return wlan_ap


def read_profiles():
    profiles = {}
    try:
        with open(NETWORK_PROFILES) as f:
            lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line and "|" in line:
                ssid, password = line.split("|", 1)
                profiles[ssid] = password
    except OSError as e:
        print("Error Reading Wifi Credentials", str(e))
        profiles = {}
    return profiles


def write_profiles(profiles):
    lines = []
    for ssid, password in profiles.items():
        lines.append("%s|%s\n" % (ssid, password))
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
    if em == 0: # force hard coded ap
        wlan_ap = run_ap(0)
        print(wlan_ap)
        print(wlan_ap.config("essid"))
        print("APEM up. Network config: ", wlan_ap.ifconfig())
        set_wlan_status(["APEM", wlan_ap])
    else:    
        # try to connect to station
        wlan_sta = get_sta_con()
        if wlan_sta is not None:
            # connected to station
            print(wlan_sta)
            print(wlan_sta.config("essid"))
            print("Connected. Network config: ", wlan_sta.ifconfig())
            set_wlan_status(["STA", wlan_sta])
        else: # open ap connection try saved ap else fixed ap
            wlan_ap = run_ap(1)
            print(wlan_ap)
            print(wlan_ap.config("essid")) 
            print("AP up. Network config: ", wlan_ap.ifconfig())
            set_wlan_status(["AP", wlan_ap])
    
    