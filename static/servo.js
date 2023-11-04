// Slider
var ch1Slider = document.querySelector("#ch1Slider");
var ch1Value = document.querySelector("#ch1Value");

var ch2Slider = document.querySelector("#ch2Slider");
var ch2Value = document.querySelector("#ch2Value");

var ch3Slider = document.querySelector("#ch3Slider");
var ch3Value = document.querySelector("#ch3Value");

// events
ch1Slider.addEventListener("input", () => {
  ch1Value.textContent = ch1Slider.value;
  sendMessage(
    JSON.stringify({
      srv1: ch1Slider.value,
      srv2: ch2Slider.value,
      srv3: ch3Slider.value,
    })
  );
});

ch2Slider.addEventListener("input", () => {
  ch2Value.textContent = ch2Slider.value;
  sendMessage(
    JSON.stringify({
      srv1: ch1Slider.value,
      srv2: ch2Slider.value,
      srv3: ch3Slider.value,
    })
  );
});

ch3Slider.addEventListener("input", () => {
  ch3Value.textContent = ch3Slider.value;
  sendMessage(
    JSON.stringify({
      srv1: ch1Slider.value,
      srv2: ch2Slider.value,
      srv3: ch3Slider.value,
    })
  );
});

// servo page ready
function srvpageready() {
  sendMessage(JSON.stringify({"wpg":"2"}));
  console.log("Servo page ready");
}

// WebSocket support
var targetUrl = `ws://${location.host}/servo/ws`;
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
  srvpageready(); 
}
function onClose(event) {
  console.log("Closing connection to server..");
  setTimeout(initializeSocket, 2000);
}
function onMessage(event) {
  console.log("WebSocket message received:", event);
}

function sendMessage(message) {
  websocket.send(message);
}
