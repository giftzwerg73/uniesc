# ***** export list with ESC-Info *****
esclist = []
def get_esclist():
    global esclist
    return esclist


# ***** tables for hobbywing esc *****
class HW_WP8BL150_Module:
    def __init__(self):
        self.ESCName = "HW QuickRun WP8BL150"
        self.ItemName = ["Running Mode",
                         "Drag Brake Force",
                         "Low Voltage Cut-Off",
                         "Start Mode(Punch)",
                         "Max Brake Force"]
        self.ItemValue = [["Forward with Brake", "Forward/Reverse with Brake", "Forward and Reverse"],
                          ["0%", "5%", "10%", "20%", "40%", "60%", "80%", "100%"],
                          ["Non-Protection", "2.6V/Cell", "2.8V/Cell", "3.0V/Cell", "3.2V/Cell", "3.4V/Cell"],
                          ["Level1", "Level2", "Level3", "Level4", "Level5", "Level6", "Level7", "Level8", "Level9"],
                          ["25%", "50%", "75%", "100%", "Disable"]]

        self.EscAuthor = "Author: MS, 03.10.2023"
        self.ItemNr = len(self.ItemName)
        self.ValNr = []
        for x in range(0, self.ItemNr):
            self.ValNr.append(len(self.ItemValue[x]) - 1)


class HW_MAX8_Module:
    def __init__(self):
        self.ESCName = "HW EZRUN MAX8"
        self.ItemName = ["Running Mode",
                         "LiPo Cells",
                         "Cutoff Voltage",
                         "ESC Thermal Protection",
                         "Motor Thermal Protection",
                         "Motor Rotation",
                         "BEC Voltage",
                         "Brake Force",
                         "Reverse Force",
                         "Start Mode (Punch)",
                         "Drag Brake"]
        self.ItemValue = [["Forward with Brake", "Forward/Reverse with Brake", "Forward and Reverse"],
                          ["Auto Calculation", "2S", "3S", "4S", "6S"],
                          ["Disabled", "Auto (Low)", "Auto (Intermediate)", "Auto (High)"],
                          ["105℃/221°F", "125℃/257°F"],
                          ["Disabled", "105℃/221°F", "125℃/257°F"],
                          ["CCW", "CW"],
                          ["6.0V", "7.4V"],
                          ["12.5%", "25%", "37.5%", "50.0%", "62.5%", "75.0%", "87.5%", "100.0%", "Disabled"],
                          ["25%", "50%"],
                          ["Level1", "Level2", "Level3", "Level4", "Level5"],
                          ["0%", "2%", "4%", "6%", "8%", "10%", "12%", "14%", "16%"]]
        self.EscAuthor = "Author: MS, 03.10.2023"
        self.ItemNr = len(self.ItemName)
        self.ValNr = []
        for x in range(0, self.ItemNr):
            self.ValNr.append(len(self.ItemValue[x]) - 1)


class HW_MAX10_SCT_MODULE:
    def __init__(self):
        self.ESCName = "HW EZRUN MAX10 SCT"
        self.ItemName = ["Running Mode",
                         "LiPo Cells",
                         "Cutoff Voltage",
                         "ESC Thermal Protection",
                         "Motor Thermal Protection",
                         "Motor Rotation",
                         "BEC Voltage",
                         "Brake Force",
                         "Reverse Force",
                         "Start Mode (Punch)",
                         "Drag Brake"]
        self.ItemValue = [["Forward with Brake", "Forward/Reverse with Brake"],
                          ["Auto Calculation", "2S", "3S", "4S"],
                          ["Disabled", "Auto (Low)", "Auto (Intermediate)", "Auto (High)"],
                          ["105℃/221°F", "125℃/257°F"],
                          ["Disabled", "105℃/221°F", "125℃/257°F"],
                          ["CCW", "CW"],
                          ["6.0V", "7.4V"],
                          ["12.5%", "25%", "37.5%", "50.0%", "62.5%", "75.0%", "87.5%", "100.0%", "Disabled"],
                          ["25%", "50%"],
                          ["Level1", "Level2", "Level3", "Level4", "Level5"],
                          ["0%", "2%", "4%", "6%", "8%", "10%", "12%", "14%", "16%"]]

        self.EscAuthor = "Author: MS, 09.02.2024"
        self.ItemNr = len(self.ItemName)
        self.ValNr = []
        for x in range(0, self.ItemNr):
            self.ValNr.append(len(self.ItemValue[x]) - 1)


# ***** tables for team magic esc *****  
class TM_WP8BL100_Module:
    def __init__(self):
        self.ESCName = "Team Magic WP-8BL100-RTR"
        self.ItemName = ["Running Mode",
                         "Drag Brake Force",
                         "Low Voltage Cut-Off",
                         "Start Mode(Punch)",
                         "Max Brake Force"]
        self.ItemValue = [["Forward with Brake", "Forward/Reverse with Brake", "Forward and Reverse"],
                          ["0%", "5%", "10%", "20%", "40%", "60%", "80%", "100%"],
                          ["Non-Protection", "2.6V/Cell", "2.8V/Cell", "3.0V/Cell", "3.2V/Cell", "3.4V/Cell"],
                          ["Level1", "Level2", "Level3", "Level4", "Level5", "Level6", "Level7", "Level8", "Level9"],
                          ["25%", "50%", "75%", "100%", "Disable"]]

        self.EscAuthor = "Author: MS, 03.10.2023"
        self.ItemNr = len(self.ItemName)
        self.ValNr = []
        for x in range(0, self.ItemNr):
            self.ValNr.append(len(self.ItemValue[x]) - 1)


class TM_WP8BL150_Module:
    def __init__(self):
        self.ESCName = "Team Magic WP-8BL150-RTR"
        self.ItemName = ["Running Mode",
                         "Drag Brake Force",
                         "Low Voltage Cut-Off",
                         "Start Mode(Punch)",
                         "Max Brake Force"]
        self.ItemValue = [["Forward with Brake", "Forward/Reverse with Brake", "Forward and Reverse"],
                          ["0%", "5%", "10%", "20%", "40%", "60%", "80%", "100%"],
                          ["Non-Protection", "2.6V/Cell", "2.8V/Cell", "3.0V/Cell", "3.2V/Cell", "3.4V/Cell"],
                          ["Level1", "Level2", "Level3", "Level4", "Level5", "Level6", "Level7", "Level8", "Level9"],
                          ["25%", "50%", "75%", "100%", "Disable"]]

        self.EscAuthor = "Author: MS, 03.10.2023"
        self.ItemNr = len(self.ItemName)
        self.ValNr = []
        for x in range(0, self.ItemNr):
            self.ValNr.append(len(self.ItemValue[x]) - 1)


# ***** tables for team orion esc *****
class TO_BRAINZ8_Module:
    def __init__(self):
        self.ESCName = "Team Orion BRAINZ8 BLS120A"
        self.ItemName = ["Running Mode",
                         "Drag Brake Force",
                         "Low Voltage Cut-Off",
                         "Start Mode(Punch)",
                         "Max Brake Force"]
        self.ItemValue = [["Forward with Brake", "Forward/Reverse with Brake", "Forward and Reverse"],
                          ["0%", "5%", "10%", "20%", "40%", "60%", "80%", "100%"],
                          ["Non-Protection", "2.6V/Cell", "2.8V/Cell", "3.0V/Cell", "3.2V/Cell", "3.4V/Cell"],
                          ["Level1", "Level2", "Level3", "Level4", "Level5", "Level6", "Level7", "Level8", "Level9"],
                          ["25%", "50%", "75%", "100%", "Disable"]]

        self.EscAuthor = "Author: MS, 03.10.2023"
        self.ItemNr = len(self.ItemName)
        self.ValNr = []
        for x in range(0, self.ItemNr):
            self.ValNr.append(len(self.ItemValue[x]) - 1)


# ***** tables for arrma esc *****      
class ARRMA_BLX185_Module:
    def __init__(self):
        self.ESCName = "ARRMA BLX185"
        self.ItemName = ["Low Voltage Cut-Off",
                         "Punch Setting",
                         "Brake Strength",
                         "Running Mode",
                         "Motor Rotation"]
        self.ItemValue = [["LIPO", "NIMH"],
                          ["Level1", "Level2", "Level3", "Level4", "Level5", "Level6", "Level7", "Level8", "Level9"],
                          ["25%", "37.5%", "50%"],
                          ["Fwd/Brk", "Fwd/Brk/Rev"],         
                          ["Reverse (CW)", "Normal (CCW)"]]

        self.EscAuthor = "Author: MS, 03.10.2023"
        self.ItemNr = len(self.ItemName)
        self.ValNr = []
        for x in range(0, self.ItemNr):
            self.ValNr.append(len(self.ItemValue[x]) - 1)
            
            
 
# ***** make big list of all ESCs ***** 
# hobbywing esc
esclist.append(HW_WP8BL150_Module())
esclist.append(HW_MAX8_Module())
esclist.append(HW_MAX10_SCT_MODULE())
# team magic esc
esclist.append(TM_WP8BL100_Module())
esclist.append(TM_WP8BL150_Module())
# kosho esc
esclist.append(TO_BRAINZ8_Module())
# arrma esc
esclist.append(ARRMA_BLX185_Module())







