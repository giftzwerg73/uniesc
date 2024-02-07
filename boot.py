from machine import Pin
from time import sleep_ms
from esc_com import read_init, read_gpio


# debug
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
       
       
