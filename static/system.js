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
  get_message(event.data);
}

function sendMessage(message) {
  websocket.send(message);
}

function get_message(data) {
    var selssid = document.getElementById("selectssid");
    var opt = document.createElement("option");
    var wifbtn = document.getElementById("wifibtn");
    var updbtn = document.getElementById("updatebtn");
    var msg = JSON.parse(data);
    if ("wif" in msg) {     
        if (msg["wif"] == "scan start") {
            // remove old scan
            var len = selssid.length - 1;
            for(var i=len; i>1; i--) {
                console.log("remove option: ", selssid[i]);
                selssid.remove(i);
            }
        }
    }
    if ("sid" in msg) {
        opt.text = msg["sid"]
        console.log("add option: ", opt);
        selssid.add(opt);
    }
    if ("wifcol" in msg) {
        if (msg["wifcol"] == "btngreen") {
           wifbtn.style.backgroundColor = 'green';
        }
        if (msg["wifcol"] == "btnred") {
           wifbtn.style.backgroundColor = 'red';
        }
        if (msg["wifcol"] == "btnyellow") {
           wifbtn.style.backgroundColor = 'yellow';
        }
        if (msg["wifcol"] == "btngrey") {
           wifbtn.style.backgroundColor = '#d1d1d1';
        }
        if (msg["wifcol"] == "btnblue") {
           wifbtn.style.backgroundColor = 'blue';
        }
    }
    if ("otacol" in msg) { 
        if (msg["otacol"] == "btngrey") {
           updbtn.style.backgroundColor = '#d1d1d1';
        }
        if (msg["otacol"] == "btnblue") {
           updbtn.style.backgroundColor = 'blue';
        }
        if (msg["otacol"] == "btngreen") {
           updbtn.style.backgroundColor = 'green';
        }
        if (msg["otacol"] == "btnyellow") {
           updbtn.style.backgroundColor = 'yellow';
        }
        if (msg["otacol"] == "btnred") {
           updbtn.style.backgroundColor = 'red';
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

function fnbtnremove() {
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
      "wif": "remove",
      "ssid": ssid,
      "pw": pw,
    })
  );
  console.log("Button Remove");
}

function fnbtnota() {
  sendMessage(JSON.stringify({"ota":"update"}));
  console.log("Button Update");
}
