from machine import Pin
from time import sleep_us
from esc_com import read_init, gen_test_data

# debug
# from esc_com import read_gpio
# read_gpio()


# usb power WL_GPIO2   	intern
usbpwr = Pin("WL_GPIO2", Pin.IN).value()
led = Pin("LED", Pin.OUT, value=1)

if usbpwr == 0:
    while True:
        led.on()
        ret = read_init()
        if ret == 0:
            print("Init success")
            for x in range(0, 5):
                led.toggle()
                sleep_us(250*1000)
            led.on()
            break
        else:
            for x in range(0, 15):
                led.toggle()
                sleep_us(100*1000)
            led.on()
            print("Retry Init...\n")


# import other needed stuff
from machine import Timer
from wificon import wifi_connect, get_wlan_status
from esc_com import usb_init
import os
import ugit

# check for updates
update = 0
try:
    f = open('update.dat', 'r')
    upf = f.read()
    f.close()
    os.remove('update.dat')
    if upf is "run update":
        update = 1
except OSError:  # open file failed -> no update go on
    pass

# blink timer
timled = Timer()

if update == 0 and usbpwr == 1:
    timled.init(freq=7, mode=Timer.PERIODIC, callback=lambda t:led.toggle())
    if usb_init() == 1:
        timled.deinit()
        while True:
            led.on()
            try:
                ret = read_init()
            except KeyboardInterrupt:
                gen_test_data(1)
                print("")
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print("Skipping read_init()")          
                print("Warning: Using invalid generated Testdata")
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print("")
                ret = 0  
            if ret == 0:
                print("Init success")
                for x in range(0, 5):
                    led.toggle()
                    sleep_us(250*1000)
                led.on()
                break
            else:
                for x in range(0, 15):
                    led.toggle()
                    sleep_us(100*1000)
                led.on()
                print("Retry Init...\n")
    else:
        timled.deinit()  

 
# make network connection
wifi_connect()
wstat = get_wlan_status()
if wstat[0] == "STA":
    # check update
    if update == 1:
        chk = ugit.check_update_version() 
        if chk is True:   # if version differs
            timled.init(freq=5, mode=Timer.PERIODIC, callback=lambda t:led.toggle())
            print("Running update now...")
            ugit.pull_all(isconnected=True,reboot=True)
            while True:
                pass

    blinkfreq = 1
elif wstat[0] == "AP":
    blinkfreq = 2
else:
    blinkfreq = 13 

timled.init(freq=blinkfreq, mode=Timer.PERIODIC, callback=lambda t:led.toggle())
