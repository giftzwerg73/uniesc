// system page ready
function systempageready() {
  sendMessage(JSON.stringify({"wpg":"3"}));
  console.log("System page ready");
}

// WebSocket support
var targetUrl = `ws://${location.host}/system/ws`;
var websocket;
window.addEventListener("load", onLoad);

function onLoad() {
  initializeSocket();
}

function initializeSocket() {
  console.log("Opening WebSocket connection MicroPython Server...");
  websocket = new WebSocket(targetUrl);
  websocket.onopen = onOpen;
  websocket.onclose = onClose;
  websocket.onmessage = onMessage;
}
function onOpen(event) {
  console.log("Starting connection to WebSocket server..");
  systempageready(); 
}
function onClose(event) {
  console.log("Closing connection to server..");
  setTimeout(initializeSocket, 2000);
}
function onMessage(event) {
  console.log("WebSocket message received:", event);
  updateSSID(event.data);
  colorsave(event.data);
  colorupdate(event.data);
}

function sendMessage(message) {
  websocket.send(message);
}

function updateSSID(data) {
   var x = document.getElementById("selectssid");
   var opt = document.createElement("option");
   var ssidtxt = JSON.parse(data);
   if ("wif" in ssidtxt) {
     if (ssidtxt["wif"] == "scan start") {
       // remove old scan
       var len = x.length - 1;
       for(var i=len; i>1; i--) {
         console.log("remove option: ", x[i]);
         x.remove(i);
       }
     }
   }
   if ("sid" in ssidtxt) {
     opt.text = ssidtxt["sid"]
     console.log("add option: ", opt);
     x.add(opt);
     
   }
}

function colorsave(data) {
    var btncolorwifi = JSON.parse(data);
    if ("wifcol" in btncolorwifi) {
        var x = document.getElementById("wifibtn");
        if (btncolorwifi["wifcol"] == "btngreen") {
           x.style.backgroundColor = 'green';
        }
        if (btncolorwifi["wifcol"] == "btnred") {
           x.style.backgroundColor = 'red';
        }
        if (btncolorwifi["wifcol"] == "btnyellow") {
           x.style.backgroundColor = 'yellow';
        }
        if (btncolorwifi["wifcol"] == "btngrey") {
           x.style.backgroundColor = '#d1d1d1';
        }
        if (btncolorwifi["wifcol"] == "btnblue") {
           x.style.backgroundColor = 'blue';
        }
    }
}
 
function colorupdate(data) {
    var btncolorupdate = JSON.parse(data);
    if ("otacol" in btncolorupdate) {
        var x = document.getElementById("updatebtn");
        if (btncolorupdate["otacol"] == "btngrey") {
           x.style.backgroundColor = '#d1d1d1';
        }
        if (btncolorupdate["otacol"] == "btnblue") {
           x.style.backgroundColor = 'blue';
        }
        if (btncolorupdate["otacol"] == "btngreen") {
           x.style.backgroundColor = 'green';
        }
        if (btncolorupdate["otacol"] == "btnyellow") {
           x.style.backgroundColor = 'yellow';
        }
        if (btncolorupdate["otacol"] == "btnred") {
           x.style.backgroundColor = 'red';
        }
    }
}
 
function isEmpty(value) {
  return (value == null || (typeof value === "string" && value.trim().length === 0));
}

function fnbtnscan() {
  sendMessage(JSON.stringify({"wif":"scan"}));
  console.log("Button Scan");
}

function fnbtnsave() {
  let customssid = document.getElementById("customssid").value;
  let selectssid = document.getElementById("selectssid").value;
  let pw = document.getElementById("pw").value;
  console.log(customssid);
  console.log(selectssid);
  console.log(pw);
  var ssid = ""
  if (!isEmpty(customssid)) {
      ssid = customssid;
  }
  if (!isEmpty(selectssid)) {
      ssid = selectssid;
  }
  
  sendMessage(
    JSON.stringify({
      "wif": "save",
      "ssid": ssid,
      "pw": pw,
    })
  );
  console.log("Button Connect");
}

function fnbtnota() {
  sendMessage(JSON.stringify({"ota":"update"}));
  console.log("Button Update");
}
