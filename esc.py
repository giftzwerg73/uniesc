from machine import Pin, PWM, UART
from time import sleep
from debug import dbgprint

esclist = []
EscListNr = 0

class TM_WP8BL100_Module:
    def __init__(self):
        self.ItemValue = [ ["ESC Type", "Team Magic WP-8BL100-RTR"],
                           ["Running Mode", "Forward with Brake", "Forward/Reverse with Brake", "Forward and Reverse"],
                           ["Drag Brake Force", "0%", "5%", "10%", "20%", "40%", "60%", "80%", "100%"],
                           ["Low Voltage Cut-Off Threshold", "Non-Protection", "2.6V/Cell", "2.8V/Cell", "3.0V/Cell", "3.2V/Cell", "3.4V/Cell"],
                           ["Start Mode(Punch)", "Level1", "Level2", "Level3", "Level4", "Level5", "Level6", "Level7", "Level8", "Level9"],
                           ["Max Brake Force", "25%", "50%", "75%", "100%", "Disable"] ]
        
        self.EscAuthor = "Author: MS, 03.10.2023"
        self.ItemNr = len(self.ItemValue)
        self.ItmValArr = []
        for x in range(0, self.ItemNr):
           self.ItmValArr.append(1)
        
    def deinit_esc(self):
        pass
    
    def connect_esc(self):
        pass
    
    def disconnect_esc(self):
        pass
    
    def item_esc(self):
        pass
    
    def value_esc(self):
        pass
    
    def reset_esc(self):
        pass
    
    def ok_esc(self):
        pass
esclist.append(TM_WP8BL100_Module())

class TM_WP8BL150_Module:
    def __init__(self):
        self.ItemValue = [ ["ESC Type", "Team Magic WP-8BL150-RTR"],
                           ["Running Mode", "Forward with Brake", "Forward/Reverse with Brake", "Forward and Reverse"],
                           ["Drag Brake Force", "0%", "5%", "10%", "20%", "40%", "60%", "80%", "100%"],
                           ["Low Voltage Cut-Off Threshold", "Non-Protection", "2.6V/Cell", "2.8V/Cell", "3.0V/Cell", "3.2V/Cell", "3.4V/Cell"],
                           ["Start Mode(Punch)", "Level1", "Level2", "Level3", "Level4", "Level5", "Level6", "Level7", "Level8", "Level9"],
                           ["Max Brake Force", "25%", "50%", "75%", "100%", "Disable"] ]
        
        self.EscAuthor = "Author: MS, 03.10.2023"
        self.ItemNr = len(self.ItemValue)
        self.ItmValArr = []
        for x in range(0, self.ItemNr):
           self.ItmValArr.append(1)
               
    def deinit_esc(self):
        pass
    
    def connect_esc(self):
        pass
    
    def disconnect_esc(self): 
        pass
    
    def item_esc(self):
        pass
    
    def value_esc(self):
        pass
    
    def reset_esc(self):
        pass
    
    def ok_esc(self):
        pass
esclist.append(TM_WP8BL150_Module())

class HW_WP8BL150_Module:
    def __init__(self):
        self.ItemValue = [ ["ESC Type", "HW QuickRun WP8BL150"],
                           ["Running Mode", "Forward with Brake", "Forward/Reverse with Brake", "Forward and Reverse"],
                           ["Drag Brake Force", "0%", "5%", "10%", "20%", "40%", "60%", "80%", "100%"],
                           ["Low Voltage Cut-Off Threshold", "Non-Protection", "2.6V/Cell", "2.8V/Cell", "3.0V/Cell", "3.2V/Cell", "3.4V/Cell"],
                           ["Start Mode(Punch)", "Level1", "Level2", "Level3", "Level4", "Level5", "Level6", "Level7", "Level8", "Level9"],
                           ["Max Brake Force", "25%", "50%", "75%", "100%", "Disable"] ]
        
        self.EscAuthor = "Author: MS, 03.10.2023"
        self.ItemNr = len(self.ItemValue)
        self.ItmValArr = []
        for x in range(0, self.ItemNr):
           self.ItmValArr.append(1)
               
    def deinit_esc(self):
        pass
    
    def connect_esc(self):
        pass
    
    def disconnect_esc(self): 
        pass
    
    def item_esc(self):
        pass
    
    def value_esc(self):
        pass
    
    def reset_esc(self):
        pass
    
    def ok_esc(self):
        pass
esclist.append(HW_WP8BL150_Module())

class HW_MAX8_V2_Module:
    def __init__(self):
        self.ItemValue = [ ["ESC Type", "HW EZRUN MAX8 V2"],
                           ["Running Mode", "Forward with Brake", "Forward/Reverse with Brake", "Forward and Reverse"],
                           ["Drag Brake Force", "0%", "5%", "10%", "20%", "40%", "60%", "80%", "100%"],
                           ["Low Voltage Cut-Off Threshold", "Non-Protection", "2.6V/Cell", "2.8V/Cell", "3.0V/Cell", "3.2V/Cell", "3.4V/Cell"],
                           ["Start Mode(Punch)", "Level1", "Level2", "Level3", "Level4", "Level5", "Level6", "Level7", "Level8", "Level9"],
                           ["Max Brake Force", "25%", "50%", "75%", "100%", "Disable"] ]
        
        self.EscAuthor = "Author: MS, 28.10.2023"
        self.ItemNr = len(self.ItemValue)
        self.ItmValArr = []
        for x in range(0, self.ItemNr):
           self.ItmValArr.append(1)
        
    def deinit_esc(self):
        pass
    
    def connect_esc(self):
        pass
    
    def disconnect_esc(self):
        pass
    
    def item_esc(self):
        pass
    
    def value_esc(self):
        pass
    
    def reset_esc(self):
        pass
    
    def ok_esc(self):
        pass
esclist.append(HW_MAX8_V2_Module())

class KYOSHO_BRAINZ8_Module:
    def __init__(self):
        self.ItemValue = [ ["ESC Type", "KYOSHO BRAINZ8 BLS120A"],
                           ["Running Mode", "Forward with Brake", "Forward/Reverse with Brake", "Forward and Reverse"],
                           ["Drag Brake Force", "0%", "5%", "10%", "20%", "40%", "60%", "80%", "100%"],
                           ["Low Voltage Cut-Off Threshold", "Non-Protection", "2.6V/Cell", "2.8V/Cell", "3.0V/Cell", "3.2V/Cell", "3.4V/Cell"],
                           ["Start Mode(Punch)", "Level1", "Level2", "Level3", "Level4", "Level5", "Level6", "Level7", "Level8", "Level9"],
                           ["Max Brake Force", "25%", "50%", "75%", "100%", "Disable"] ]
        
        self.EscAuthor = "Author: MS, 28.10.2023"
        self.ItemNr = len(self.ItemValue)
        self.ItmValArr = []
        for x in range(0, self.ItemNr):
           self.ItmValArr.append(1)
        
    def deinit_esc(self):
        pass
    
    def connect_esc(self):
        pass
    
    def disconnect_esc(self):
        pass
    
    def item_esc(self):
        pass
    
    def value_esc(self):
        pass
    
    def reset_esc(self):
        pass
    
    def ok_esc(self):
        pass    
esclist.append(KYOSHO_BRAINZ8_Module())
     
class ARRMA_WP8BL150_Module:
    pass   

def get_esclist():
    dbgprint("")
    for esc in esclist:
        for item in esc.ItemValue:
            for value in item:     
                dbgprint(value)
        dbgprint("")
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
    dbgprint(escindex)
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
    dbgprint(ret)
    return ret

def incvalnr(escnr, itemnr, nr):
    val = nr + 1
    if val >= len(esclist[escnr].ItemValue[itemnr]):
        val = 1
    dbgprint(val)
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
    dbgprint(esclist[escnr].ItmValArr)
    lcdtxt = "Saving to ESC\r\r\rPress Ok Button to proceed..."
    return lcdtxt

def mkescreset (escnr, itemnr, valnr):
    lcdtxt = "Resetting ESC\r\r\rPress Ok Button to proceed..."
    return lcdtxt
