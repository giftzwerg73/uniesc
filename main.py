from microdot_asyncio import Microdot, Response, send_file
from microdot_utemplate import render_template
from microdot_asyncio_websocket import with_websocket
from machine import Pin
import time
import gc
import ujson
from menu import menu, resetmenu
from debug import dbgprint
from servo import SERVOModule, servoaction
from led import init_led, set_blink, init_obled, blink_obled
from wificon import scan4ap, connectnsave, get_wlan_status, get_known_stations, del_profile, save_profile
from ugit import get_version
import brand


# pinout 
# tx    GP8   Pin_11 
# rx    GP9   Pin_12
# led1  GP14  Pin_19
# led2  GP15  Pin_20
# pwm1  GP19  Pin_25
# pwm2  GP20  Pin_26
# pwm3  GP21  Pin_27

# onboard led 
obled = init_obled()

# gpio board led1, led2
led_pins = [14, 15]
init_led(led_pins, 0, 4)
set_blink(0, 0, 2, 0)
set_blink(1, 2, 0, 0)

# initialize servos
pwm_pins = [19, 20, 21]
servos = SERVOModule(pwm_pins, 300000, 2300000, 50)
# Set default position to 90 degree
# servo.turn_off_servo()
servos.set_servo_pos({'srv1': '90', 'srv2': '90', 'srv3': '90'})

# Initialize MicroDot
app = Microdot()
Response.default_content_type = 'text/html'

# root route
@app.route('/')
async def index(request):
    return render_template('index.html')

@app.route('/esc.html')
async def esc(request):
    resetmenu()
    return render_template('esc.html')

@app.route('/servo.html')
async def servo(request):
    return render_template('servo.html')

@app.route('/system.html')
async def wifi(request):
    return render_template('system.html')

@app.route('/about.html')
async def about(request):
    tmp = []
    fwver = get_version().split(":")
    tmp.append("FW: " + fwver[1])
    tmp.append("HW: " + brand.HWREF)
    tmp.append("Serial: " + brand.SERIAL)
    essid = get_wlan_status()[1].config('ssid')
    ip = get_wlan_status()[1].ifconfig()[0]
    tmp.append("WLAN: "+ essid + " " + ip)
    mac = get_wlan_status()[1].config('mac')
    tmp.append("MAC: " + '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(*mac))
    return render_template('about.html', infolist=tmp)


# initialize websocket
@app.route('esc/ws')
@with_websocket
async def esc(request, ws):
    while True:
        gc.collect()
        data = await ws.receive()
        obled.on()
        ujdata = ujson.loads(data)
        dbgprint(ujdata) 
        lcdtxt = menu(ujdata)
        if lcdtxt != None:
            await ws.send(ujson.dumps({"lcd1":lcdtxt}))
        obled.off()

@app.route('servo/ws')
@with_websocket
async def servo(request, ws):
    while True:
        gc.collect()
        data = await ws.receive()
        obled.on()
        ujdata = ujson.loads(data)
        dbgprint(ujdata)
        servoans = servoaction(servos, ujdata)
        if servoans != None:
            await ws.send(ujson.dumps({"srv":servoans}))
        obled.off()
       
@app.route('system/ws')
@with_websocket
async def system(request, ws):
    while True:
        gc.collect()
        data = await ws.receive()
        obled.on()
        ujdata = ujson.loads(data)
        dbgprint(ujdata)
        if "wpg" in ujdata:
            if ujdata["wpg"] is "3": # websocket for system page ready
                await ws.send(ujson.dumps({"wifcol":"btngrey", "otacol":"btngrey"}))
            else:
                await ws.send(ujson.dumps({"wpg":"err"}))    
        elif "wif" in ujdata:
            # try connect and save to wifi.dat
            if ujdata["wif"] == "scan":
                await ws.send(ujson.dumps({"wif":"scan start", "wifcol":"btnyellow"}))
                scanssids = scan4ap()
                savedssid = list(get_known_stations().keys())
                rmonlyssids = []
                for ssid in savedssid:
                    if ssid not in scanssids:
                        rmonlyssids.append(ssid + " *")
                apssid = brand.APSSID
                if apssid not in savedssid:
                    rmonlyssids.append(apssid + " +")
                ssids = []
                # from scan 
                for ssid in scanssids:
                    ssids.append(ssid)
                # from wifi.dat + ap
                for ssid in rmonlyssids:
                    ssids.append(ssid)
                dbgprint(ssids)
                while len(ssids):
                    scanssid = ssids.pop(0)
                    ssid = str(scanssid)
                    await ws.send(ujson.dumps({"sid":ssid}))
                    time.sleep(0.003)
                await ws.send(ujson.dumps({"wif":"scan stop", "wifcol":"btngrey"}))
            elif ujdata["wif"] == "remove":
                if "ssid" and "pw" in ujdata:
                    # remove from wifi.dat
                    selssid = ujdata["ssid"]
                    if selssid in rmonlyssids:
                        selssid = selssid[:-2]
                    if del_profile(selssid):
                        btncolor = "btngreen"
                    else:
                        btncolor = "btnred"
                    await ws.send(ujson.dumps({"wifcol":btncolor})) 
            elif ujdata["wif"] == "save":
                if "ssid" and "pw" in ujdata:
                    selssid = ujdata["ssid"]
                    pw = ujdata["pw"]
                    if selssid in rmonlyssids:
                         selssid = selssid[:-2]
                         if save_profile(selssid, pw):
                            await ws.send(ujson.dumps({"wifcol":"btngreen"}))
                         else:
                            await ws.send(ujson.dumps({"wifcol":"btnred"}))       
                    else: # try connect and save to wifi.dat
                        conn = connectnsave(selssid, pw)
                        if conn == True:
                            await ws.send(ujson.dumps({"wifcol":"btngreen"}))
                        elif conn == False:
                            await ws.send(ujson.dumps({"wifcol":"btnred"}))
                        elif conn == None:
                            await ws.send(ujson.dumps({"wifcol":"btnblue"}))      
            else:
                await ws.send(ujson.dumps({"wif":"err"}))
        elif "ota" in ujdata:
            if ujdata["ota"] == "update":
                stat = get_wlan_status()[0]
                if stat == "STA":
                    f = open("update.dat", "w")
                    f.write("run update")
                    f.close()
                    await ws.send(ujson.dumps({"otacol":"btngreen"}))
                    blink_obled(led, 0.1, 0.2, 3)
                    machine.reset()
                else:
                    await ws.send(ujson.dumps({"otacol":"btnyellow"}))
            else:
                await ws.send(ujson.dumps({"ota":"err"}))
        else:
            await ws.send(ujson.dumps({"sys":"err"}))
        obled.off()
        
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
        servos.deinit_pwms()
        pass
