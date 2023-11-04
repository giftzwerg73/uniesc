// esc page ready
function escpageready() {
  sendMessage(JSON.stringify({"wpg":"1"}));
  console.log("ESC page ready");
}

// buttons
function fnbtn1() {
  sendMessage(JSON.stringify({"btn":"1"}));
  console.log("Button 1");
}

function fnbtn2() {
  sendMessage(JSON.stringify({"btn":"2"}));
  console.log("Button 2");
}

function fnbtn3() {
  sendMessage(JSON.stringify({"btn":"3"}));
  console.log("Button 3");
}

function fnbtn4() {
  sendMessage(JSON.stringify({"btn":"4"}));
  console.log("Button 4");
}

// WebSocket support
var targetUrl = `ws://${location.host}/esc/ws`;
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
  escpageready();
}

function onClose(event) {
  console.log("Closing connection to server..");
  setTimeout(initializeSocket, 2000);
}

function onMessage(event) {
  console.log("WebSocket message received:", event);
  updateLCD(event.data);
}

function sendMessage(message) {
  websocket.send(message);
}

function updateLCD(data) {
  const lcdValues = document.querySelector("#lcd1");
  var lcdtxt = JSON.parse(data);
  if ("lcd1" in lcdtxt) {
    lcdValues.value = lcdtxt["lcd1"];
  }
}

