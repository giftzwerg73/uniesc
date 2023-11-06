from machine import Pin, PWM, UART
from time import sleep
     
class ARRMA_WP8BL150_Module:
    def __init__(self):
        self.ItemValue = [ ["ESC Type", "ARRMA BLS150A"],
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

