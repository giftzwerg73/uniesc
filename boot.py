from machine import Pin
from time import sleep_ms
from uniesc import read_init

# gpio
usbpwr = Pin("WL_GPIO2", Pin.IN)
escpwr = Pin("GP2", Pin.IN, Pin.PULL_UP)
onbled = Pin("LED", Pin.OUT, value=0)
rdled = Pin("GP17", Pin.OUT, value=0)
blled = Pin("GP16", Pin.OUT, value=0)
sw = Pin("GP15", Pin.IN, Pin.PULL_UP)

usbpwr_atboot = usbpwr.value()
sw_atboot = sw.value()
escpwr_atboot = escpwr.value()
# no switch at boot and power from ecs only
if sw_atboot == 1 and usbpwr_atboot == 0 and escpwr_atboot == 1:
    while True:
        rdled.on()
        ret = read_init()
        if ret == 0:   
            for x in range(0, 5):
                rdled.toggle()
                sleep_ms(250)
            break
        else:
            for x in range(0, 15):
                rdled.toggle()
                sleep_ms(100)
