from machine import Pin, PWM, UART
from esc_hw import *
from esc_tm import *
from esc_kyosho import *
from esc_arrma import *


esclist = []
EscListNr = 0

# hobbywing esc
esclist.append(HW_WP8BL150_Module())
esclist.append(HW_MAX8_V2_Module())
# team magic esc
esclist.append(TM_WP8BL100_Module())
esclist.append(TM_WP8BL150_Module())
# kosho esc
esclist.append(KYOSHO_BRAINZ8_Module())
# arrma esc
esclist.append(ARRMA_WP8BL150_Module())
       
def get_esclist():
    global esclist
    return esclist
     
def escval(escnr, itemnr, valnr):
    escitem = esclist[escnr].ItemValue[itemnr]
    val = str(escitem[valnr])
    return val

def incescnr(nr):
    global EscListNr
    
    escindex = nr + 1
    if escindex >= len(esclist):
        escindex = 0
    EscListNr = escindex
    return escindex

def get_escnr():
    global EscListNr
    return EscListNr

def incitemnr(escnr, nr):
    itm = nr + 1
    if itm >= esclist[escnr].ItemNr:
        itm = 0
    val = esclist[escnr].ItmValArr[itm]
    ret = [itm, val]
    return ret

def incvalnr(escnr, itemnr, nr):
    val = nr + 1
    if val >= len(esclist[escnr].ItemValue[itemnr]):
        val = 1
    esclist[escnr].ItmValArr[itemnr] = val
    return esclist[escnr].ItmValArr[itemnr]

def mkescscreen(escnr, itemnr, valnr):
    strmaxitem = str(esclist[escnr].ItemNr - 1)
    stritemnr = str(itemnr)
    stritemname = str(escval(escnr, itemnr, 0))
    if itemnr == 0:
        strmaxval = str(len(esclist))
        strvalnr = str(escnr + 1)
    else:
        strmaxval = str(len(esclist[escnr].ItemValue[itemnr]) - 1)
        strvalnr = str(valnr)
    strvalname = str(escval(escnr, itemnr, valnr))
    lcdtxt = "Item " + stritemnr + " (max. " + strmaxitem + "):\r"
    lcdtxt += stritemname + "\r"
    lcdtxt += "Value " + strvalnr + " (max. " + strmaxval + "):\r"
    lcdtxt += strvalname
    return lcdtxt

def mkescsave (escnr, itemnr, valnr):
    lcdtxt = "Saving to ESC\r\r\rPress Ok Button to proceed..."
    return lcdtxt

def mkescreset (escnr, itemnr, valnr):
    lcdtxt = "Resetting ESC\r\r\rPress Ok Button to proceed..."
    return lcdtxt
