import wificon
import network
from machine import Pin
from time import sleep
from debug import dbgprint
from led import init_obled, blink_obled
import ugit
import os


led = init_obled()
led.on()
wlan_sta = wificon.get_sta_con()        
if wlan_sta is None:
    # open ap
    wlan_ap = wificon.run_ap()
    print(wlan_ap)
    print("AP up. Network config: ", wlan_ap.ifconfig())
    blink_obled(led, 0.5, 0.5, 2)
else:
    # connected to ap
    print(wlan_sta)
    print("Connected. Network config: ", wlan_sta.ifconfig())
    # check for updates
    try:
        f = open('update.dat', 'r')
        upf = f.read()
        f.close()
        os.remove('update.dat')
        if upf is "run update":
            chk = ugit.check_update_version()
            if chk is True:
                print("Running update now...")
                ugit.pull_all(isconnected=True,reboot=False)
                blink_obled(led, 0.1, 0.1, 0)    
    except OSError:  # open failed -> normal boot
        pass
    
    blink_obled(led, 0.1, 0.2, 3)
      
