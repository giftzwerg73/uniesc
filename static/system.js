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
   var ssidtxt = JSON.parse(data);
   if ("sid" in ssidtxt) {
     var x = document.getElementById("selectssid");
     var option = document.createElement("option");
     if ( ssidtxt["sid"] == "scan finished") {
       if(x.value == "Scanning...") {
         x.remove(x[0]);  
       }
     } else {
       option.text = ssidtxt["sid"]
       x.add(option);
     }
   }
}

function colorsave(data) {
    var btncolorsave = JSON.parse(data);
    if ("wif" in btncolorsave) {
        var x = document.getElementById("savebtn");
        if (btncolorsave["wif"] == "connection ok") {
           x.style.backgroundColor = 'green';
        }
        if (btncolorsave["wif"] == "connection failed") {
           x.style.backgroundColor = 'red';
        }
    }
}
 
function colorupdate(data) {
    var btncolorupdate = JSON.parse(data);
    if ("ota" in btncolorupdate) {
        var x = document.getElementById("updatebtn");
        if (btncolorupdate["ota"] == "new version") {
           x.style.backgroundColor = 'blue';
        }
        if (btncolorupdate["ota"] == "ok") {
           x.style.backgroundColor = 'green';
        }
         if (btncolorupdate["ota"] == "undefined") {
           x.style.backgroundColor = 'yellow';
        }
        if (btncolorupdate["ota"] == "err") {
           x.style.backgroundColor = 'red';
        }
    }
}
 
function isEmpty(value) {
  return (value == null || (typeof value === "string" && value.trim().length === 0));
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
  console.log("Button Save");
}

function fnbtnota() {
  sendMessage(JSON.stringify({"ota":"update"}));
  console.log("Button Update");
}
