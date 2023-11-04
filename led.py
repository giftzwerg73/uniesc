from machine import Pin, Timer
from time import sleep

leds = []
onoff = []
cnt = 0
maxcnt = 0

def init_obled():
  obled = Pin("LED", Pin.OUT)
  obled.off()
  return obled

def blink_obled(gpio, ton, toff, nr):
    if nr <= 0:
        while True:
            gpio.on()
            sleep(ton)
            gpio.off()
            sleep(toff)
    else:
        while nr:
            gpio.on()
            sleep(ton)
            gpio.off()
            sleep(toff)
            nr = nr - 1

def blink_led(timer):
    global cnt
    x = 0
    for led in leds:
        lednr = onoff[x]
        if cnt == lednr[0]:
            led.toggle()
        elif cnt == lednr[1]:
            led.toggle()
        x += 1
    cnt += 1
    if cnt >= maxcnt:
        cnt = 0

def init_led(led_pins, state, freqency):
    global leds
    global onoff
    global maxcnt
    leds  = []
    onoff = []
    for pin in led_pins:
        led = Pin(pin, mode=Pin.OUT)
        led.value(state)
        leds.append(led)
        onoff.append([freqency, freqency])
    maxcnt = freqency  
    Timer().init(freq=freqency, mode=Timer.PERIODIC, callback=blink_led) 
        
def set_blink(lednr, on, off, state):
    global onoff
    if lednr < len(leds):
        leds[lednr].value(state)
        onoff[lednr] = [on, off]
