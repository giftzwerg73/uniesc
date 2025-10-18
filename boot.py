from machine import Pin
from time import sleep_us
from uniesc import read_init, gen_test_data

# gpio
usbpwr = Pin("WL_GPIO2", Pin.IN)
escpwr = Pin("GP2", Pin.IN, Pin.PULL_UP)
onbled = Pin("LED", Pin.OUT, value=1)
rdled = Pin("GP17", Pin.OUT, value=0)
blled = Pin("GP16", Pin.OUT, value=0)
sw = Pin("GP15", Pin.IN, Pin.PULL_UP)

usbpwrval = usbpwr.value()
sw_atboot = sw.value()
if sw_atboot == 1 and usbpwrval == 0 and escpwr.value() == 1:
    while True:
        rdled.on()
        ret = read_init()
        if ret == 0:   
            for x in range(0, 5):
                rdled.toggle()
                sleep_us(250*1000)
            break
        else:
            for x in range(0, 15):
                rdled.toggle()
                sleep_us(100*1000)


# import other needed stuff
from machine import Timer
from wificon import wifi_connect, get_wlan_status
import os
import ugit

# blink timer
timled = Timer()
blinkled = 1
def blink(t):
    global blinkled
    if blinkled == 1:
        rdled.toggle()
    elif blinkled == 2:
         blled.toggle()
    elif blinkled == 3:
        rdled.toggle()
        blled.toggle()
    elif blinkled == 4:
        onbled.toggle()
    else:
        rdled.toggle()
        blled.toggle()
        onbled.toggle()
        
if sw_atboot == 1 and usbpwrval == 1:
    testmode = False
    while True:
        blled.off()
        rdled.off()
        blinkled = 1
        timled.init(freq=5, mode=Timer.PERIODIC, callback=blink)
        if escpwr.value() == 1:
            print("Switch ESC off")
            while escpwr.value() == 1:
                sleep_us(3*1000)                       
        print("Switch ESC on or press button for test mode")
        while escpwr.value() == 0:
            sleep_us(3*1000)
            if sw.value() == 0:
                timled.deinit()
                blled.on()
                rdled.off()
                blinkled = 5
                timled.init(freq=7, mode=Timer.PERIODIC, callback=blink)
                while sw.value() == 0:
                    sleep_us(3*1000)
                testmode = True
                break      
        timled.deinit()
        if testmode == False:    
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
        else:
            gen_test_data(2)
            print("")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("Skipping read_init()")          
            print("Warning: Using generated Testdata")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("")
            break

# make network connection
blled.on()
rdled.on()
onbled.on()
wifi_connect(sw_atboot)
wstat = get_wlan_status()
if wstat[0] == "STA":
    try: # check for updates
        f = open('update.dat', 'r')
        upf = f.read()
        f.close()
        os.remove('update.dat')
        if upf is "run update":
            chk = ugit.check_update_version() 
            if chk is True:   # if version differs
                blled.on()
                rdled.off()
                blinkled = 3
                timled.init(freq=1, mode=Timer.PERIODIC, callback=blink)
                print("Running update now...")
                ugit.pull_all(isconnected=True,reboot=True)
                while True:
                    pass
    except OSError:  # open file failed -> no update go on
       pass
    blled.off()
    rdled.off()
    blinkled = 2
    timled.init(freq=1, mode=Timer.PERIODIC, callback=blink)
elif wstat[0] == "AP":
    blled.off()
    rdled.off()
    blinkled = 2
    timled.init(freq=3, mode=Timer.PERIODIC, callback=blink)
elif wstat[0] == "APEM":
    blled.off()
    rdled.on()
    blinkled = 3
    timled.init(freq=3, mode=Timer.PERIODIC, callback=blink)
else:
    blled.off()
    rdled.off()
    blinkled = 1
    timled.init(freq=13, mode=Timer.PERIODIC, callback=blink)
