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
from wificon import scan4ap, connectnsave
from ugit import check_update_version
    

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

@app.route('/index.html')
async def about(request):
    return render_template('index.html')


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
                await ws.send(ujson.dumps({"ota":"reset"}))
                await ws.send(ujson.dumps({"wif":"reset"}))
                ssids = scan4ap()
                while len(ssids):
                    scanssid = ssids.pop(0)
                    ssid = str(scanssid)
                    await ws.send(ujson.dumps({"sid":ssid}))
                    time.sleep(0.003)
                await ws.send(ujson.dumps({"sid":"scan finished"}))
            else:
                await ws.send(ujson.dumps({"sys":"err"}))
        elif "wif" and "ssid" and "pw" in ujdata:
            # try connect and save to wifi.dat
            if ujdata["wif"] == "save":
                ssid = ujdata["ssid"]
                pw = ujdata["pw"]
                conn = connectnsave(ssid, pw)
                if conn == True:
                    ans = "connection ok"
                elif conn == False:
                    ans = "connection failed"
                elif conn == None:
                    ans = "already connected"
            else:
                ans = "err"   
            await ws.send(ujson.dumps({"wif":ans}))
        elif "ota" in ujdata:
            if ujdata["ota"] == "update":
                chk = check_update_version()
                if chk is True:
                    f = open("update.dat", "w")
                    f.write("run update")
                    f.close()
                    await ws.send(ujson.dumps({"ota":"new version"}))
                    blink_obled(led, 0.1, 0.1, 15)
                    machine.reset()
                elif chk is False:
                    await ws.send(ujson.dumps({"ota":"ok"}))
                elif chk is None:
                    await ws.send(ujson.dumps({"ota":"undefined"}))
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


