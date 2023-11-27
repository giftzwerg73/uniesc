import time
from esc import get_esclist, escval, incitemnr, incescnr, incvalnr, decescnr, decvalnr, mkescscreen, mkescsave, mkescreset
from debug import dbgprint

esc = 0
item = 0
value = 1
menu = 0
init = 0

def menu(data):
    global item
    global value
    global esc
    global menu
    global init
    
    if "wpg" in data:
        if data["wpg"] is "1": # websocket for esc page ready
            esc = 0
            item = 0
            value = 1
            menu = 0
            init = 0
            lcdtxt = mkescscreen(esc, item, value)
            return lcdtxt
        else:
            return None
    elif "btn" in data: # known by menu
        pass
    else: # unknown
        return None
    
        
    if menu == -1: # test datas and lcd
        if data["btn"] is "1":
             lcdtxt = "Item\rwas pressed"
        elif data["btn"] is "2":
             lcdtxt = "-Value-\rwas pressed"
        elif data["btn"] is "3":
            lcdtxt = "+Value+\rwas pressed"
        elif data["btn"] is "4":
            lcdtxt = "Ok\rwas pressed"
        else:
            lcdtxt = "No data\rwas pressed"
        return lcdtxt
    elif menu == 0: # get esc by name
        if data["btn"] is "1":
            ret = incitemnr(esc, item)
            item = ret[0]
            value = ret[1]
            menu = 1
            if init == 0:
               dbgprint("Now init hw for esc programming try to connect and read params...")
               init = 1
            lcdtxt = mkescscreen(esc, item, value)
            return lcdtxt
        if data["btn"] is "2":
            esc = decescnr(esc)
            item = 0
            value = 1
            init = 0
            lcdtxt = mkescscreen(esc, item, value)
            return lcdtxt
        if data["btn"] is "3":
            esc = incescnr(esc)
            item = 0
            value = 1
            init = 0
            lcdtxt = mkescscreen(esc, item, value)
            return lcdtxt
        if data["btn"] is "4":
            pass
        return None
    elif menu == 1:
        if data["btn"] is "1":
           ret = incitemnr(esc, item)
           item = ret[0]
           value = ret[1]
           if item == 0: #select esc by name
                menu = 0
                lcdtxt = mkescscreen(esc, item, value)
                return lcdtxt
           else:
               lcdtxt = mkescscreen(esc, item, value)
               return lcdtxt
        if data["btn"] is "2":
           value = decvalnr(esc, item, value)
           lcdtxt = mkescscreen(esc, item, value)
           return lcdtxt
        if data["btn"] is "3":
           value = incvalnr(esc, item, value)
           lcdtxt = mkescscreen(esc, item, value)
           return lcdtxt
        if data["btn"] is "4":
           if str(escval(esc, item, 0)) == "Reset ESC": # reset
               if str(escval(esc, item, value)) == "Yes":
                   value = 1 # set value to No
                   lcdtxt = mkescreset(esc, item, value)
                   menu = 2
                   return lcdtxt
           else: # save
               lcdtxt = mkescsave(esc, item, value)
               menu = 2
               return lcdtxt
        return None
    elif menu == 2:
        if data["btn"] is "4":
            lcdtxt = mkescscreen(esc, item, value)
            menu = 1
            return lcdtxt
        return None
    else: # ???
        return None

def resetmenu():
    global item
    global value
    global esc
    global menu
    global init
    esc = 0
    item = 0
    value = 1
    menu = 0
    init = 0
    
