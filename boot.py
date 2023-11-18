import wificon
import network
from machine import Pin
from time import sleep
from debug import dbgprint
from led import init_obled, blink_obled
import ugit
import os

# pinout 
# tx    GP8   Pin_11 
# rx    GP9   Pin_12
# led1  GP14  Pin_19
# led2  GP15  Pin_20
# pwm1  GP19  Pin_25
# pwm2  GP20  Pin_26
# pwm3  GP21  Pin_27

led = init_obled()
led.on()
rxgpio = Pin(9, Pin.IN, Pin.PULL_UP)

if rxgpio.value() == 1:
    # nomal start
    wlan_sta = wificon.get_sta_con()        
    if wlan_sta is None:
        # open ap
        wlan_ap = wificon.run_ap(False)
        print(wlan_ap)
        print("AP up. Network config: ", wlan_ap.ifconfig())
        wificon.set_wlan_status(["AP", wlan_ap])
        blink_obled(led, 0.5, 0.5, 3)
    else:
        # connected to ap
        print(wlan_sta)
        print("Connected. Network config: ", wlan_sta.ifconfig())
        wificon.set_wlan_status(["STA", wlan_sta])
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
else:
    # open ap with defaults
    print("start AP with defaults")
    wlan_ap = wificon.run_ap(True)
    print(wlan_ap)
    print("AP up. Network config: ", wlan_ap.ifconfig())
    wificon.set_wlan_status(["AP", wlan_ap])
    blink_obled(led, 0.05, 0.05, 23)
