import displayio
import random
import Apps
import board

class Procedural(Apps.App):
    def __init__(self, macropad):
        self.macropad = macropad
        self.name = "Procedural thing"

    def scramble(self, bitmap, noise_density=50):
        for x in range(1, bitmap.width-1):
            for y in range(1, bitmap.height-1):
                randomInt = random.randint(0,100)
                if randomInt>noise_density:
                    bitmap[x, y] = 0
                else:
                    bitmap[x, y] = 1

    def updateGrid(self, old, new): # old and new bitmap # also assumes out of bounds are all =1
        width = old.width
        height = old.height

        for y in range(1, height-1):
            for x in range(1, width-1):
                sum = old[x-1, y-1] + old[x, y-1] + old[x+1, y-1] + old[x-1, y] + old[x+1, y] + old[x-1, y+1] + old[x, y+1] + old[x+1, y+1]
                if sum>4:
                    new[x,y] = 1
                else:
                    new[x,y] = 0

    def applyAutomaton(self, group1, group2, bitmap1, bitmap2, board, iterations):
        curr = True # for flip flop
        while iterations+1>0:
            if curr:
                board.DISPLAY.root_group = group1 #set root group
                self.updateGrid(bitmap1, bitmap2)
            else:
                board.DISPLAY.root_group = group2 #set root group
                self.updateGrid(bitmap2, bitmap1)

            curr = not curr

            iterations = iterations - 1




    def run(self): 
        iterat = 15

        macropad = self.macropad

        group1 = displayio.Group() # create group
        group2 = displayio.Group()

        bitmap1 = displayio.Bitmap(128, 64, 2)
        bitmap2 = displayio.Bitmap(128, 64, 2)
        bitmap1.fill(1)
        bitmap2.fill(1)

        palette = displayio.Palette(2) #2 colors
        palette[0] = 0x000000 # set colors for pallete
        palette[1] = 0xFFFFFF

        tiles1 = displayio.TileGrid(bitmap1, pixel_shader=palette) # create tile grid using bitmap and palette
        tiles2 = displayio.TileGrid(bitmap2, pixel_shader=palette)

        group1.append(tiles1) # append tiles to group, to be displayed
        group2.append(tiles2)

        self.scramble(bitmap1, 60)

        self.applyAutomaton(group1, group2, bitmap1, bitmap2, board, 8)
        
        while True:
            if macropad.encoder_switch == 1:
                break

        