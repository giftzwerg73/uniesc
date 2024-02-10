from machine import Pin
from time import sleep_ms
from esc_com import read_init

# debug
# from esc_com import read_gpio
# read_gpio()

led = Pin("LED", Pin.OUT)
while True:
    led.on()
    ret = read_init()
    if ret == 0:
        print("Init success")
        for x in range(0, 5):
            led.toggle()
            sleep_ms(250)
        led.on()
        break
    else:
        for x in range(0, 15):
            led.toggle()
            sleep_ms(100)
        led.on()
        print("Retry Init...\n")


# import other needed stuff
from machine import Timer
from wificon import wifi_connect, get_wlan_status
import os
import ugit

# now blink
timled = Timer()

def blink(timer):
    led.toggle() 

# make network connection
wifi_connect()
wstat = get_wlan_status()
if wstat[0] == "STA":
    # check for updates
    try:
        f = open('update.dat', 'r')
        upf = f.read()
        f.close()
        os.remove('update.dat')
        if upf is "run update":
            chk = ugit.check_update_version() 
            if chk is True:   # if version differs
                timled.init(freq=0.33, mode=Timer.PERIODIC, callback=blink)
                print("Running update now...")
                ugit.pull_all(isconnected=True,reboot=True)  
    except OSError:  # open file failed -> normal boot
        pass   
    blinkfreq = 1
elif wstat[0] == "AP":
    blinkfreq = 2
else:
    blinkfreq = 13 

timled.init(freq=blinkfreq, mode=Timer.PERIODIC, callback=blink)
