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

console.log(esc_data[3]);
    
function get_esc_select() {  
    var e =  document.getElementById("escname");
    var value = e.value;
    esc_selname = e.options[e.selectedIndex].text;
    console.log(esc_selname);
}

function checknrnames(list_names) {
    var nritems = esc_data[1];
    var ret = 1;
    var lenitems = 0;
    var lenvals = 0;
    lenitems = list_names[0].length;
    if ((nritems+1) == lenitems) { // nr items ok
       for (x=0;x<=nritems;x++) {
         lenvals = list_names[1][x].length;
         if ((esc_data[2][x]+1) != lenvals) {
             ret = 0;
         }
       }
    } else {
        ret = 0;
    }
    return ret; 
}

function mkdisp() {
  if (esc_isinit == 1) {
    get_esc_select()
    var listname = esc_dict[esc_selname]
    if (esc_selname == "None")
    {
        for (x=0;x<=esc_data[1];x++) {
            var valcnt = esc_data[2][x];
            var valnr = esc_data[3][x];
            var itemnrstr = x+1
            var selidstr = "Item " + itemnrstr.toString();
            var lblidstr = "LBL_" + selidstr;
            var item = document.getElementById(selidstr);
            var lbl = document.getElementById(lblidstr);
            var itemstr = "Item " + itemnrstr.toString();
            // rename label
            lbl.textContent = itemstr;
            // remove old value options for item
            while (item.options.length > 0) {
                item.remove(0);
            }
            // add options for item
            for (val=0;val<=valcnt;val++) {
                var opt = document.createElement("option");
                var valnrstr = val+1
                opt.text = "Value " + valnrstr.toString();
                item.add(opt);
            }
            // set actual value
            item.options.selectedIndex = valnr;
        }
    } else {
      // check if names fit nr items and nr values
      if( checknrnames(listname) == 1) { 
        document.getElementById("info").value = "Selected: " + esc_selname;
        for (x=0;x<=esc_data[1];x++) {
            var valcnt = esc_data[2][x];
            var valnr = esc_data[3][x];
            var itemnrstr = x+1
            var selidstr = "Item " + itemnrstr.toString();
            var lblidstr = "LBL_" + selidstr;
            var item = document.getElementById(selidstr);
            var lbl = document.getElementById(lblidstr);
            var itemstr = "Item " + itemnrstr.toString() + " : " + listname[0][x];
            // rename label
            lbl.textContent = itemstr;
            // remove old value options for item
            while (item.options.length > 0) {
                item.remove(0);
            }
            // add options for item
            for (val=0;val<=valcnt;val++) {
                var opt = document.createElement("option");
                var valnrstr = val+1
                opt.text = "Value " + valnrstr.toString() + " : " + listname[1][x][val];
                item.add(opt);
            }
            // set actual value
            item.options.selectedIndex = valnr;
        }
      } else { // names mismatch esc_data 
          console.log("Names missmatch")
          document.getElementById("info").value = "ESC NAMES MISSMATCH!!!"; 
      }
    }
  }
}

function update_escdata(onchgsel) {
    var getselectindex = onchgsel.options.selectedIndex;
    var mysplitid = onchgsel.id.split("Item ");
    var getselectitemnr = parseInt(mysplitid[1] - 1);
    esc_data[3][getselectitemnr] = getselectindex;
    console.log(esc_data[3]);
}
    
function save() {
  if (esc_isinit == 1) {
    sendMessage(JSON.stringify({"save": esc_data[3]}));
    document.getElementById("info").value = "Saving Data...";
    console.log("Saving Data");
    console.log(esc_data[3]);
  }
}

function reset() {
  if (esc_isinit == 1) {
	esc_data[3] = Array.from(esc_data[4]);
	mkdisp();
	document.getElementById("info").value = "Reset to Defaults";
    console.log(esc_data[3]);
  }
}

function got_answer(data) {
  var ans = JSON.parse(data);
  if ("saved" in ans) {
    if (ans["saved"] != "ok") {
      console.log(ans["saved"]);
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
      mkdisp()
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

