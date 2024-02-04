# ***** tables for hobbywing esc *****
class HW_WP8BL150_Module:
    def __init__(self):
        self.ESCName = "HW QuickRun WP8BL150"
        self.ItemName = ["Running Mode", "Drag Brake Force", "Low Voltage Cut-Off", "Start Mode(Punch)", "Max Brake Force"]
        self.ItemValue = [ ["Forward with Brake", "Forward/Reverse with Brake", "Forward and Reverse"],
                           ["0%", "5%", "10%", "20%", "40%", "60%", "80%", "100%"],
                           ["Non-Protection", "2.6V/Cell", "2.8V/Cell", "3.0V/Cell", "3.2V/Cell", "3.4V/Cell"],
                           ["Level1", "Level2", "Level3", "Level4", "Level5", "Level6", "Level7", "Level8", "Level9"],
                           ["25%", "50%", "75%", "100%", "Disable"] ] 
                           
        
        self.EscAuthor = "Author: MS, 03.10.2023"
        self.ItemNr = len(self.ItemName)
        self.ValNr = []
        for x in range(0, self.ItemNr):
           self.ValNr.append(len(self.ItemValue[x])-1)
               

class HW_MAX8_V2_Module:
    def __init__(self):
        self.ESCName = "HW EZRUN MAX8 V2"
        self.ItemName = ["Running Mode", "Drag Brake Force","Low Voltage Cut-Off", "Start Mode(Punch)", "Max Brake Force"]
        self.ItemValue = [ ["Forward with Brake", "Forward/Reverse with Brake", "Forward and Reverse"],
                           ["0%", "5%", "10%", "20%", "40%", "60%", "80%", "100%"],
                           ["Non-Protection", "2.6V/Cell", "2.8V/Cell", "3.0V/Cell", "3.2V/Cell", "3.4V/Cell"],
                           ["Level1", "Level2", "Level3", "Level4", "Level5", "Level6", "Level7", "Level8", "Level9"],
                           ["25%", "50%", "75%", "100%", "Disable"] ]

        self.EscAuthor = "Author: MS, 03.10.2023"
        self.ItemNr = len(self.ItemName)
        self.ValNr = []
        for x in range(0, self.ItemNr):
           self.ValNr.append(len(self.ItemValue[x])-1)
      
      
# ***** tables for team magic esc *****  
class TM_WP8BL100_Module:
    def __init__(self):
        self.ESCName = "Team Magic WP-8BL100-RTR"
        self.ItemName = ["Running Mode", "Drag Brake Force","Low Voltage Cut-Off", "Start Mode(Punch)", "Max Brake Force"]
        self.ItemValue = [ ["Forward with Brake", "Forward/Reverse with Brake", "Forward and Reverse"],
                           ["0%", "5%", "10%", "20%", "40%", "60%", "80%", "100%"],
                           ["Non-Protection", "2.6V/Cell", "2.8V/Cell", "3.0V/Cell", "3.2V/Cell", "3.4V/Cell"],
                           ["Level1", "Level2", "Level3", "Level4", "Level5", "Level6", "Level7", "Level8", "Level9"],
                           ["25%", "50%", "75%", "100%", "Disable"] ]

        
        self.EscAuthor = "Author: MS, 03.10.2023"
        self.ItemNr = len(self.ItemName)
        self.ValNr = []
        for x in range(0, self.ItemNr):
           self.ValNr.append(len(self.ItemValue[x])-1)
        

class TM_WP8BL150_Module:
    def __init__(self):
        self.ESCName = "Team Magic WP-8BL150-RTR"
        self.ItemName = ["Running Mode", "Drag Brake Force","Low Voltage Cut-Off", "Start Mode(Punch)", "Max Brake Force"]
        self.ItemValue = [ ["Forward with Brake", "Forward/Reverse with Brake", "Forward and Reverse"],
                           ["0%", "5%", "10%", "20%", "40%", "60%", "80%", "100%"],
                           ["Non-Protection", "2.6V/Cell", "2.8V/Cell", "3.0V/Cell", "3.2V/Cell", "3.4V/Cell"],
                           ["Level1", "Level2", "Level3", "Level4", "Level5", "Level6", "Level7", "Level8", "Level9"],
                           ["25%", "50%", "75%", "100%", "Disable"] ]

        
        self.EscAuthor = "Author: MS, 03.10.2023"
        self.ItemNr = len(self.ItemName)
        self.ValNr = []
        for x in range(0, self.ItemNr):
           self.ValNr.append(len(self.ItemValue[x])-1)


# ***** tables for team orion esc *****
class TO_BRAINZ8_Module:
    def __init__(self):
        self.ESCName = "Team Orion BRAINZ8 BLS120A"
        self.ItemName = ["Running Mode", "Drag Brake Force","Low Voltage Cut-Off", "Start Mode(Punch)", "Max Brake Force"]
        self.ItemValue = [ ["Forward with Brake", "Forward/Reverse with Brake", "Forward and Reverse"],
                           ["0%", "5%", "10%", "20%", "40%", "60%", "80%", "100%"],
                           ["Non-Protection", "2.6V/Cell", "2.8V/Cell", "3.0V/Cell", "3.2V/Cell", "3.4V/Cell"],
                           ["Level1", "Level2", "Level3", "Level4", "Level5", "Level6", "Level7", "Level8", "Level9"],
                           ["25%", "50%", "75%", "100%", "Disable"] ]

        
        self.EscAuthor = "Author: MS, 03.10.2023"
        self.ItemNr = len(self.ItemName)
        self.ValNr = []
        for x in range(0, self.ItemNr):
           self.ValNr.append(len(self.ItemValue[x])-1)
        
    
# ***** tables for arrma esc *****      
class ARRMA_WP8BL150_Module:
    def __init__(self):
        self.ESCName = "ARRMA BLS185"
        self.ItemName = ["Running Mode", "Drag Brake Force","Low Voltage Cut-Off", "Start Mode(Punch)", "Max Brake Force"]
        self.ItemValue = [ ["Forward with Brake", "Forward/Reverse with Brake", "Forward and Reverse"],
                           ["0%", "5%", "10%", "20%", "40%", "60%", "80%", "100%"],
                           ["Non-Protection", "2.6V/Cell", "2.8V/Cell", "3.0V/Cell", "3.2V/Cell", "3.4V/Cell"],
                           ["Level1", "Level2", "Level3", "Level4", "Level5", "Level6", "Level7", "Level8", "Level9"],
                           ["25%", "50%", "75%", "100%", "Disable"] ]
        
        self.EscAuthor = "Author: MS, 03.10.2023"
        self.ItemNr = len(self.ItemName)
        self.ValNr = []
        for x in range(0, self.ItemNr):
           self.ValNr.append(len(self.ItemValue[x])-1)
           