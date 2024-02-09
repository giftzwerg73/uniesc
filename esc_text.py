from esc_tables import *

esclist = []
EscListNr = 0

# hobbywing esc
esclist.append(HW_WP8BL150_Module())
esclist.append(HW_MAX8_V2_Module())
esclist.append(HW_MAX10_SCT_MODULE())
# team magic esc
esclist.append(TM_WP8BL100_Module())
esclist.append(TM_WP8BL150_Module())
# kosho esc
esclist.append(TO_BRAINZ8_Module())
# arrma esc
esclist.append(ARRMA_WP8BL150_Module())
       
def get_esclist():
    global esclist
    return esclist

def get_escnamelist():
    global esclist
    escnamelist = []
    for x in range(0, len(esclist)):
        escnamelist.append(esclist[x].ESCName)
    return escnamelist

def get_escitemtextlist():
    global esclist
    escitemtextlist = []
    for x in range(0, len(esclist)):
        escitemtextlist.append(esclist[x].ItemName)
    return escitemtextlist

def get_escvaluetextlist():
    global esclist
    escvaluetextlist = []
    for x in range(0, len(esclist)):
        escvaluetextlist.append(esclist[x].ItemValue)
    return escvaluetextlist
    
def get_escname(escnr):
    global esclist
    escname = esclist[escnr].ESCName
    return escname
    
def get_escitemname(escnr, itemnr):
    global esclist
    escitemname = esclist[escnr].ItemName[itemnr]
    return escitemname
    
def get_escitemvalname(escnr, itemnr, valnr):
    global esclist
    escitemvalname = esclist[escnr].ItemValue[itemnr][valnr]
    return escitemvalname

def get_esctabledict():
    global esclist
    esctabledict = {}
    # { ESCNAME1: [[itemlist] ,[[valuelistitem1], [valuelistitem2], ...], ESCNAME2: [.... }
    for x in range(0, len(esclist)):
        dictlist = []
        dictlist.append(esclist[x].ItemName)
        dictlist.append(esclist[x].ItemValue)    
        esctabledict[esclist[x].ESCName] = dictlist
    return esctabledict
        
    
def test_esctabledict(name, item, value, tabledict):
    print(tabledict[name])
    print(tabledict[name][0][item])
    print(tabledict[name][1][item][value])
    
    
    
    


