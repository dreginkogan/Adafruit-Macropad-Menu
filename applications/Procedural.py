import displayio
import random
import Apps
import board

class Procedural(Apps.App):
    def __init__(self, macropad):
        self.macropad = macropad
        self.name = "Procedural thing"

    def run(self):
        
        