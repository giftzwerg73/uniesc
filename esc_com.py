from machine import Pin, Timer
from time import sleep_us, ticks_us, ticks_diff, ticks_add

# tx    GP13   Pin_17 
# rx    GP14   Pin_19
txgpio = Pin("GP13", Pin.OUT, value=0)
rxgpio = Pin("GP14", Pin.IN, Pin.PULL_UP)

init_ok = 0
items = 0
options_per_item = [0] * 15
read_values = [0] * 15
reset_values = [0] * 15
ack = 0

tmocnt = 0
def inctmo(timer):
    global tmocnt
    tmocnt += 1  
  

def get_init_data():
    global init_ok, items, options_per_item, read_values, reset_values, ack
    return [init_ok, items, options_per_item, read_values, reset_values, ack]


def set_init_data(status, data):
    global init_ok, items, options_per_item, read_values, reset_values, ack
    init_ok = status
    items = data[15]
    options_per_item = data[31:46]
    read_values = data[0:15]
    reset_values = data[16:31]
    ack = data[46]


def read_gpio():
    lastval = rxgpio.value()
    print("start " + str(lastval))
    while True:
        actval = rxgpio.value()
        if lastval != actval:
            edgeticks = ticks_us()
            lastval = actval
            print(str(edgeticks) + " " + str(actval))
            

def read_data(): 
    ticksstart = 0
    tickssync = 0
    rxbyte = 0
    while rxgpio.value() == 0: 	# wait for inverted start
        pass
    while rxgpio.value() == 1: 	# wait while inverted low
        pass
    tickssync = ticks_us()
    while rxgpio.value() == 0: 	# synctbit inverted high
        pass
    ticksstart = ticks_us()
    # print(ticksstart)
    bitticks = ticks_diff(ticksstart, tickssync)
    # print(bitticks)
    
    sample = ticks_add(ticksstart, 750)
    end = ticks_add(ticksstart, bitticks)
    while ticks_diff(sample, ticks_us()) > 0:
        pass
    if rxgpio.value() == 0: # startbit
        print("Startbit error")
        return None
    while ticks_diff(end, ticks_us()) > 0:
        pass
    ticksstart = ticks_add(ticksstart, bitticks)
    
    for x in range(0, 8): # databits
        sample = ticks_add(ticksstart, 750)
        end = ticks_add(ticksstart, bitticks)
        while ticks_diff(sample, ticks_us()) > 0:
            pass
        if rxgpio.value():
            rxbyte |= 0 << 8
        else:
            rxbyte |= 1 << 8  
        rxbyte >>= 1
        #tmp = ticks_us()
        #print(tmp)
        while ticks_diff(end, ticks_us()) > 0:
            pass
        ticksstart = ticks_add(ticksstart, bitticks)
    
    sample = ticks_add(ticksstart, 750)
    while ticks_diff(sample, ticks_us()) > 0:
        pass
    if rxgpio.value() == 1: # stopbit
        print("Stopbit error")
        return None
    
    return rxbyte


def write_data(data):
    txgpio.value(1)
    sleep_us(2000)
    txgpio.value(0)
    sleep_us(2000)
    txgpio.value(1)
    sleep_us(2000)
    for x in range(0, 8):
        if data & 0x01:
            txgpio.value(0)
        else:
            txgpio.value(1)
        data >>= 1
        sleep_us(2000)
    txgpio.value(0)
    sleep_us(2000)
    

def write_parameter(data):
    for x in range(0, 15):
       write_data(data[x])
    write_data(85) # write ack
    sleep_us(100)
    ack = read_data()
    if ack == 85:
        print("Set Parameter done")
        return 0
    else:
        print("Set Parameter failed")
        return -1


def read_init():  
    generte_testdata = True # False
    debug = 0
    init_data = [0] * 50
    
    if generte_testdata:
        _init_ok = 1
        _items = 4
        _options_per_item = [2, 7, 5, 8, 4, 3, 3, 2, 7, 1, 1, 5, 0, 0, 0]
        _read_values = [1, 0, 5, 4, 1, 1, 1, 1, 4, 0, 0, 0, 0, 0, 0]
        _reset_values = [1, 0, 3, 4, 1, 1, 1, 1, 4, 0, 0, 0, 0, 0, 0]
        _ack = 85
        init_data[0:15] = _read_values
        init_data[15] = _items
        init_data[16:31] = _reset_values 
        init_data[31:46] = _options_per_item 
        init_data[46] = _ack
        set_init_data(_init_ok, init_data)
        print("")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("Warning: Using generated Testdata")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("")
        return 0
       
    if rxgpio.value() == 0:
        print("Switch ESC OFF")
        while rxgpio.value() == 0:
            pass
    print("Switch ESC ON")
    while rxgpio.value() == 1:
        pass
    for x in range (0, 47):
        val = read_data()
        if val != None:
            init_data[x] = val
        else:
            print("Init failed")
            set_init_data(0, init_data)
            return -1
    if debug != 0:
        print(init_data) 
        nr_item = init_data[15]+1
        print("Nr. of Items: " + str(nr_item))
        if nr_item > 15:
            print("Nr. of Items to big")
        else:
            nr = 1
            for x in range(31, 31+nr_item):  
                print("Item " + str(nr) + " -> Nr. Options: " + str(init_data[x]+1))
                nr = nr + 1
            nr = 1
            for x in range(16, 16+nr_item):  
                print("Reset Value Item" + str(nr) + ": " + str(init_data[x]+1))
                nr = nr + 1
            nr = 1
            for x in range(0, nr_item):  
                print("Value Item "+ str(nr) + ": " + str(init_data[x]+1))
                nr = nr + 1
    else:
        sleep_us(10*1000)
    if init_data[46] == 85 and init_data[15] < 15:
        print("Send ack")
        sleep_us(90*1000)
        write_data(85) # send ack
        set_init_data(1, init_data)
        return 0
    else:
        print("Init failed")
        set_init_data(0, init_data)
        return -1
    
    


