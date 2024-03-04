from machine import Pin
from time import sleep_us
from uniesc import read_init, gen_test_data

# gpio
usbpwr = Pin("WL_GPIO2", Pin.IN)
escpwr = Pin("GP2", Pin.IN)
onbled = Pin("LED", Pin.OUT, value=0)
rdled = Pin("GP16", Pin.OUT, value=0)
blled = Pin("GP17", Pin.OUT, value=0)
sw = Pin("GP15", Pin.IN, Pin.PULL_UP)

usbpwrval = usbpwr.value()
if usbpwrval == 0 and escpwr.value() == 1:
    while True:
        rdled.on()
        ret = read_init()
        if ret == 0:   
            for x in range(0, 5):
                rdled.toggle()
                sleep_us(250*1000)
            print("Init success")
            break
        else:
            for x in range(0, 15):
                rdled.toggle()
                sleep_us(100*1000)
            print("Retry Init...\n")


# import other needed stuff
from machine import Timer
from wificon import wifi_connect, get_wlan_status
import os
import ugit

# blink timer
def blink(red, blue):
    if red:
        rdled.toggle()
    if blue:
        blled.toggle()

#switch
def sw_irq_handler():
    if sw.value() == 0:
        raise KeyboardInterrupt
 
timled = Timer()
sw.irq(trigger=Pin.IRQ_FALLING, handler=sw_irq_handler())

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

if update == 0 and usbpwrval == 1:
    timled.init(freq=5, mode=Timer.PERIODIC, callback=blink(True,False))
    try:
        while True:  
            if escpwr.value() == 1:
                print("Switch ESC off")
                while escpwr.value() == 1:
                    pass
            print("Switch ESC on")
            while escpwr.value() == 0:
                pass
            timled.deinit()
            
            rdled.on()
            ret = read_init()
            if ret == 0:
                for x in range(0, 5):
                    rdled.toggle()
                    sleep_us(250*1000)
                print("Init success")
                break
            else:
                for x in range(0, 15):
                    rdled.toggle()
                    sleep_us(100*1000)
                print("Retry Init...\n")
    except KeyboardInterrupt:
        gen_test_data(2)
        print("")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("Skipping read_init()")          
        print("Warning: Using generated Testdata")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("")
        timled.deinit()
    
    
# make network connection
blled.on()
rdled.on()
wifi_connect()
wstat = get_wlan_status()
if wstat[0] == "STA":
    # check update
    if update == 1:
        chk = ugit.check_update_version() 
        if chk is True:   # if version differs
            blled.on()
            rdled.off()
            timled.init(freq=2, mode=Timer.PERIODIC, callback=blink(True,True))
            print("Running update now...")
            ugit.pull_all(isconnected=True,reboot=True)
            while True:
                pass
    timled.init(freq=1, mode=Timer.PERIODIC, callback=blink(False,True))
elif wstat[0] == "AP":
    timled.init(freq=3, mode=Timer.PERIODIC, callback=blink(False,True))
else:
    blled.off()
    timled.init(freq=13, mode=Timer.PERIODIC, callback=blink(True,False))
