var edit_item = 0;
var esc_selname = "None";
var esc_isinit = 0;
var esc_data = [];
var esc_names = [];
var esc_dict = {};

/* 
var esc_data = [ 1,
				 4,
				[2, 7, 5, 8, 4, 3, 3, 2, 7, 1, 1, 5, 0, 0, 0],
				[1, 0, 5, 4, 1, 1, 1, 1, 4, 0, 0, 0, 0, 0, 0],
				[1, 0, 3, 4, 1, 1, 1, 1, 4, 0, 0, 0, 0, 0, 0],
				 85 ];
*/

document.getElementById("nri").value = "--";
document.getElementById("nrv").value = "--";
document.getElementById("txti").value = "--"
document.getElementById("txtv").value = "--";
console.log(esc_data[3]);
    
function get_esc_select() {  
    var e =  document.getElementById("escname");
    var value = e.value;
    esc_selname = e.options[e.selectedIndex].text;
    console.log(esc_selname);
}

function mkdisp()
{
  if (esc_isinit == 1) {
    get_esc_select()
    var listname = esc_dict[esc_selname]
    var itemnr = edit_item
    var valnr = esc_data[3][itemnr]
    if (esc_selname == "None")
    {
        document.getElementById("nri").value = itemnr + 1;
        document.getElementById("nrv").value = valnr + 1;
        document.getElementById("txti").value = "--"
        document.getElementById("txtv").value = "--";
    } else {
        document.getElementById("nri").value = itemnr + 1;
        document.getElementById("nrv").value = valnr + 1;
        document.getElementById("txti").value = listname[0][itemnr];
        document.getElementById("txtv").value = listname[1][itemnr][valnr];
    }
  }
}
    
function inc_item() {
  if (esc_isinit == 1) {
	if (edit_item < esc_data[1])
	{
		edit_item++;
	}
    mkdisp();
    console.log(esc_data[3]);
  }
}
 
function dec_item() {
  if (esc_isinit == 1) {
	if (edit_item >  0)
	{
		edit_item--; 
	}
    mkdisp();
    console.log(esc_data[3]);
  }
}

function inc_val() {
  if (esc_isinit == 1) {
	if (esc_data[3][edit_item] < esc_data[2][edit_item])
	{
		esc_data[3][edit_item]++;
	}
    mkdisp();
    console.log(esc_data[3]);
  }
}
 
function dec_val() {
  if (esc_isinit == 1) {
	if (esc_data[3][edit_item] > 0 )
	{
		esc_data[3][edit_item]--;
	}
    mkdisp();
    console.log(esc_data[3]);
  }
}
 
function save() {
  if (esc_isinit == 1) {
	document.getElementById("txti").value = "Saving to ESC";
    document.getElementById("txtv").value = "-------";
    sendMessage(JSON.stringify({"save": esc_data[3]}));
    console.log("Saving data:");
    console.log(esc_data[3]);
  }
}

function reset() {
  if (esc_isinit == 1) {
	esc_data[3] = Array.from(esc_data[4]);
    document.getElementById("nri").value = edit_item + 1;
    document.getElementById("nrv").value = esc_data[3][edit_item] + 1;
    document.getElementById("txti").value = "Values Resetted";
    document.getElementById("txtv").value = "Press Save to write to ESC";
    console.log(esc_data[3]);
  }
}

function got_answer(data) {
  var ans = JSON.parse(data);
  if ("saved" in ans) {
    if (ans["saved"] == "ok") {
      document.getElementById("txtv").value = "Done";
    } else {
      document.getElementById("txtv").value = "Error";
    }
  }
  if ("init" in ans) {
      esc_data = Array.from(ans["init"][0]);
      esc_names = Array.from(ans["init"][1]);
      Object.assign(esc_dict, ans["init"][2]);
      esc_isinit = 1;
      console.log(esc_data);
      console.log(esc_names);
      console.log(esc_dict);
      edit_item = 0;
      document.getElementById("nri").value = edit_item + 1;
      document.getElementById("nrv").value = esc_data[3][edit_item] + 1;
      document.getElementById("txti").value = "Choose ESC from List";
      document.getElementById("txtv").value = "Unknown ESC";
  } 
  if ("info" in ans) {
      document.getElementById("info").value = ans["info"];
  }
}

// WebSocket support
var targetUrl = `ws://${location.host}/ws`;
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
  sendMessage(JSON.stringify({"init": "???"}));
}

function onClose(event) {
  console.log("Closing connection to server..");
  setTimeout(initializeSocket, 2000);
}

function onMessage(event) {
  console.log("WebSocket message received:", event);
  got_answer(event.data) 
}

function sendMessage(message) {
  websocket.send(message);
}

