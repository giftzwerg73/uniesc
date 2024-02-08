from machine import Pin, Timer
import os
import time
import ujson
import config
from esc_com import get_init_data, write_parameter
from esc_text import get_escnamelist, get_escitemtextlist, get_escvaluetextlist, get_esctabledict, test_esctabledict
from wificon import wifi_connect, get_wlan_status, scan4ap, get_known_stations, save_profile, del_profile
import ugit
from microdot_asyncio import Microdot, Response, send_file
from microdot_utemplate import render_template
from microdot_asyncio_websocket import with_websocket


escdata = get_init_data()
print(escdata)
escnames = get_escnamelist()
print(escnames)
esctabledict = get_esctabledict()
print(esctabledict)
print("")
print("---------------------------------------------------------------------")
print("")


led = Pin("LED", Pin.OUT) 
def blink(timer):
    led.toggle()  

# make network connection
wifi_connect()
# now blink
wstat = get_wlan_status()
if wstat[0] == "STA":
    blinkfreq = 1
elif wstat[0] == "AP":
    blinkfreq = 2
else:
    blinkfreq = 13 
Timer().init(freq=blinkfreq, mode=Timer.PERIODIC, callback=blink)    

# Initialize MicroDot
app = Microdot()
Response.default_content_type = 'text/html'

# root route
@app.route('/')
async def index(request):
    # render in esc names
    return render_template('index.html', infolist=escnames)

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
                if write_parameter(pld) == 0: # write data to esc
                    escdata[3] = pld
                    print("Written data:")
                    print(escdata[3]) # update data
                    await ws.send(ujson.dumps({"saved": "ok"}))
                else:
                    await ws.send(ujson.dumps({"saved": "error", "info": "Saving Failed"}))
            else:
                await ws.send(ujson.dumps({"saved": "error", "info": "Data NOT valid"}))
                        
        elif "init" in ujdata:
            init_data = []
            if ujdata["init"] == "???":
                if escdata[0] == 1:
                    init_data.append(escdata)
                    init_data.append(escnames)
                    init_data.append(esctabledict)
                    await ws.send(ujson.dumps({"init": init_data}))
                    info = "Init from " + str(config.SERIAL) + " OK"
                else:
                    info = "Init from " + str(config.SERIAL) + " FAILED"
                await ws.send(ujson.dumps({"info": info}))
                
            else:
                await ws.send(ujson.dumps({"info": "Init Failed"}))
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
            if ujdata["wpg"] is "system": # websocket for system page ready
                await ws.send(ujson.dumps({"info":"Ready"}))
            else:
                await ws.send(ujson.dumps({"info":"wpg:???"}))    
        elif "wif" in ujdata:
            # try connect and save to wifi.dat
            if ujdata["wif"] == "scan":
                await ws.send(ujson.dumps({"wif":"scan start", "info":"Scan running"}))
                scanssids = scan4ap()
                savedssids = list(get_known_stations().keys())
                apssid = config.APSSID
                ssids = []  
                for i in scanssids:
                    if i not in savedssids:  		
                        status = "s ) "				# only in scan list
                    else:							
                        status = "sf) "			   	# in scan and saved list 
                    ssids.append(status + i)    
                for i in savedssids:
                    if i != apssid:
                        if i not in scanssids:
                            status = "f ) "			# only in saved list and not ap
                            ssids.append(status + i)  
                if apssid not in savedssids:
                    status = "a ) "      			# ap not in saved list
                else:
                    status = "af) "   				# ap in saved list
                ssids.append(status + apssid)
                print(ssids)
                while len(ssids):
                    ssid = str(ssids.pop(0))
                    await ws.send(ujson.dumps({"sid":ssid}))
                    time.sleep(0.003)
                await ws.send(ujson.dumps({"wif":"scan stop", "info":"Scan finished"}))
            elif ujdata["wif"] == "remove":
                if "ssid" and "pw" in ujdata:
                    # remove from wifi.dat
                    selssid = ujdata["ssid"]
                    if del_profile(selssid):
                        info = str(selssid) + " removed from list"
                    else:
                        info = str(selssid) + " remove failed"
                    await ws.send(ujson.dumps({"info":info})) 
            elif ujdata["wif"] == "save":
                if "ssid" and "pw" in ujdata:
                    selssid = ujdata["ssid"]
                    pw = ujdata["pw"]
                    save_profile(selssid, pw)
                    info = str(selssid) + " saved to file"
                    await ws.send(ujson.dumps({"info":info}))       
                     
            else:
                await ws.send(ujson.dumps({"info":"wif:???"}))
        elif "ota" in ujdata:
            if ujdata["ota"] == "update":
                stat = get_wlan_status()
                if stat[0] == "STA":
                    f = open("update.dat", "w")
                    f.write("run update")
                    f.close()
                    await ws.send(ujson.dumps({"info":"Running Update"}))
                    time.sleep(3)
                    machine.reset()
                else:
                    await ws.send(ujson.dumps({"info":"No Internet connection"}))
            else:
                await ws.send(ujson.dumps({"info":"ota:???"}))
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
