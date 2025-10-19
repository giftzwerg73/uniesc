import time
import config
import os
import ugit
import gc
from machine import Pin, Timer
from uniesc import read_init, gen_test_data
from wificon import wifi_connect, get_wlan_status, scan4ap, get_known_stations, save_profile, del_profile


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

def wait_sw_released():
    global blinkled
    bl = blled.value()
    rd = rdled.value()
    gr = onbled.value()
    blled.on()
    rdled.off()
    onbled.on()
    blinkled = 5
    timled.init(freq=7, mode=Timer.PERIODIC, callback=blink)
    while sw.value() == 0:
        sleep_ms(3)
    timled.deinit()
    blled.value(bl)
    rdled.value(rd)
    onbled.value(gr)

update = 0
skip_force_apem = 1
if sw_atboot == 0: # switch at boot
    skip_force_apem = 0
    try: # check for updates
        f = open('update.dat', 'r')
        upf = f.read()
        f.close()
        os.remove('update.dat')
        if upf is "run update":
            update = 1
            skip_force_apem = 1
    except OSError:  # open file failed -> no update go on
       pass
    wait_sw_released()
   
if update == 0 and usbpwr_atboot == 1: # no update and power from usb
    testmode = False
    while True:
        blled.off()
        rdled.off()
        onbled.off()
        blinkled = 1
        timled.init(freq=5, mode=Timer.PERIODIC, callback=blink)
        if escpwr.value() == 1:
            print("Switch ESC off")
            while escpwr.value() == 1:
                sleep_ms(3)                       
        print("Switch ESC on or press button for test mode")
        while escpwr.value() == 0:
            sleep_ms(3)
            if sw.value() == 0:
                timled.deinit()
                wait_sw_released() 
                testmode = True
                break      
        if testmode == False:
            timled.deinit()
            blled.off()
            rdled.off()
            onbled.off()
            rdled.on()
            ret = read_init()
            if ret == 0:
                for x in range(0, 5):
                    rdled.toggle()
                    sleep_ms(250)
                print("Init success")
                break
            else:
                for x in range(0, 15):
                    rdled.toggle()
                    sleep_ms(100)
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
wifi_connect(skip_force_apem)
wstat = get_wlan_status()
if wstat[0] == "STA":
    if update == 0:
        blled.off()
        rdled.off()
        blinkled = 2
        timled.init(freq=1, mode=Timer.PERIODIC, callback=blink)
    else:
        gc.collect()
        chk = ugit.check_update_version() 
        if chk is True:   # if version differs
            for x in range(0, 9):
                blled.off()
                rdled.off()
                onbled.off()
                sleep_ms(450)
                blled.on()
                rdled.on()
                onbled.on()
                sleep_ms(50)
            print("Running update now...")
            ugit.pull_all(isconnected=True,reboot=True)
            while True:
                pass    
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
    

#now import other stuff
import ujson
from microdot_asyncio import Microdot, Response, send_file
from microdot_utemplate import render_template
from microdot_asyncio_websocket import with_websocket
from uniesc import get_init_data, write_parameter, read_gpio
from esc_text import get_escnamelist, get_esctabledict, test_esctabledict

escdata = get_init_data()
escnames = get_escnamelist()
esctabledict = get_esctabledict()

print(escdata)
print(escnames)
print(esctabledict)
print("")
print("---------------------------------------------------------------------")
print("")


# Initialize MicroDot
app = Microdot()
Response.default_content_type = 'text/html'


# root route
@app.route('/')
async def index(request):
    # render in esc names and items to select
    itemnrlist = []
    for x in range(1, escdata[1]+2):
        item = "Item " + str(x)
        itemnrlist.append(item)
    return render_template('index.html', escnamelist=escnames, itemlist=itemnrlist)


# system route
@app.route('/system.html')
async def system(request):
    return render_template('system.html')


# initialize websocket for index page
@app.route('/ws')
@with_websocket
async def esc(request, ws):
    while True:
        data = await ws.receive()
        ujdata = ujson.loads(data)
        if "save" in ujdata:
            pld = ujdata["save"]
            if len(pld) == 15:
                print("Saving data...")
                try: 
                  if write_parameter(pld) == 0:  # write data to esc
                    escdata[3] = pld
                    print("Written data:")
                    print(escdata[3])  # update data
                    await ws.send(ujson.dumps({"saved": "ok", "info": "Saving Done"}))
                  else:
                    await ws.send(ujson.dumps({"saved": "error", "info": "Saving Failed"}))
                except KeyboardInterrupt:
                    await ws.send(ujson.dumps({"saved": "error", "info": "Saving Aborted"}))
            else:
                await ws.send(ujson.dumps({"saved": "error", "info": "Data NOT valid"}))

        elif "init" in ujdata:
            init_data = []
            if ujdata["init"] == "???":
                if escdata[0] == 1: # valid
                    init_data.append(escdata)
                    init_data.append(escnames)
                    init_data.append(esctabledict)
                    await ws.send(ujson.dumps({"init": init_data}))
                    info = "Init from " + str(config.SERIAL) + " OK"
                elif escdata[0] == 2: # simulated
                    init_data.append(escdata)
                    init_data.append(escnames)
                    init_data.append(esctabledict)
                    await ws.send(ujson.dumps({"init": init_data}))
                    info = "Init from " + str(config.SERIAL) + " Simulated"
                else:
                    info = "Init from " + str(config.SERIAL) + " Failed"
                await ws.send(ujson.dumps({"info": info}))
            else:
                await ws.send(ujson.dumps({"info": "Init Request Failed"}))
        else:
            await ws.send(ujson.dumps({"info": "Unknown Command"}))


# initialize websocket for system page
@app.route('system/ws')
@with_websocket
async def sys(request, ws):
    while True:
        data = await ws.receive()
        ujdata = ujson.loads(data)
        if "wpg" in ujdata:
            if ujdata["wpg"] is "system":  # websocket for system page ready
                wsta = get_wlan_status()
                consid = wsta[1].config("essid")
                conip = wsta[1].ifconfig()[0]
                fwver = ugit.get_version().split(":")[1]
                sysinfo = "Wifi " + consid + " " + conip + ", FW" + fwver + ", HW" + config.HWREF + ", SN" + config.SERIAL
                info = "Info: " + sysinfo
                await ws.send(ujson.dumps({"info": info}))
            else:
                await ws.send(ujson.dumps({"info": "wpg:???"}))
        elif "wif" in ujdata:
            # try connect and save to wifi.dat
            if ujdata["wif"] == "scan":
                await ws.send(ujson.dumps({"wif": "scan start", "info": "Scan Running"}))
                scanssids = scan4ap()
                savedssids = list(get_known_stations().keys())
                apssid = config.APSSID
                ssids = []
                for i in scanssids:
                    if i not in savedssids:
                        status = "s ) "  # only in scan list
                    else:
                        status = "sf) "  # in scan and saved list
                    ssids.append(status + i)
                for i in savedssids:
                    if i != apssid:
                        if i not in scanssids:
                            status = "f ) "  # only in saved list and not ap
                            ssids.append(status + i)
                if apssid not in savedssids:
                    status = "a ) "  # ap not in saved list
                else:
                    status = "af) "  # ap in saved list
                ssids.append(status + apssid)
                print(ssids)
                while len(ssids):
                    ssid = str(ssids.pop(0))
                    await ws.send(ujson.dumps({"sid": ssid}))
                    time.sleep_ms(3)
                await ws.send(ujson.dumps({"wif": "scan stop", "info": "Scan Finished"}))
            elif ujdata["wif"] == "remove":
                if "ssid" and "pw" in ujdata:
                    # remove from wifi.dat
                    selssid = ujdata["ssid"]
                    if del_profile(selssid):
                        info = str(selssid) + " removed from List"
                    else:
                        info = str(selssid) + " remove Failed"
                    await ws.send(ujson.dumps({"info": info}))
            elif ujdata["wif"] == "save":
                if "ssid" and "pw" in ujdata:
                    selssid = ujdata["ssid"]
                    pw = ujdata["pw"]
                    save_profile(selssid, pw)
                    info = str(selssid) + " saved to File"
                    await ws.send(ujson.dumps({"info": info}))
            else:
                await ws.send(ujson.dumps({"info": "wif:???"}))
        elif "analyze" in ujdata:
            if ujdata["analyze"] == "run":
                if Pin("WL_GPIO2", Pin.IN).value() == 1:
                    await ws.send(ujson.dumps({"info": "Running COM Analyzer"}))
                    print("")
                    print("COM-Edge Analyzer Started")
                    print("{")
                    while True:
                        try:
                            read_gpio()
                        except KeyboardInterrupt:
                            await ws.send(ujson.dumps({"info": "Break COM Analyzer"}))
                        try:
                            time.sleep_ms(3000)
                            await ws.send(ujson.dumps({"info": "Restarting COM Analyzer"}))
                        except KeyboardInterrupt:
                            break
                    print("}")
                    print("COM-Edge Analyzer Stopped")
                    print("")
                    await ws.send(ujson.dumps({"info": "COM Analyzer Stopped"}))
                else:
                    await ws.send(ujson.dumps({"info": "Connect to USB first"}))
            else:
                await ws.send(ujson.dumps({"info": "analyze:???"}))       
        elif "ota" in ujdata:
            if ujdata["ota"] == "update":
                stat = get_wlan_status()
                if stat[0] == "STA":
                    f = open("update.dat", "w")
                    f.write("run update")
                    f.close()
                    await ws.send(ujson.dumps({"info": "Running Update"}))
                    time.sleep_ms(3000)
                    machine.reset()
                else:
                    await ws.send(ujson.dumps({"info": "No Internet Connection"}))
            else:
                await ws.send(ujson.dumps({"info": "ota:???"}))
        else:
            await ws.send(ujson.dumps({"info": "Unknown Command"}))


# Static CSS/JSS
@app.route("/static/<path:path>")
def static(request, path):
    if ".." in path:
        # directory traversal is not allowed
        return "Not found", 404
    return send_file("static/" + path)


# shutdown
@app.get('/shutdown')
def shutdown(request):
    request.app.shutdown()
    return 'The server is shutting down...'


if __name__ == "__main__":
    try:
        app.run(port=80)
    except KeyboardInterrupt:
        pass
