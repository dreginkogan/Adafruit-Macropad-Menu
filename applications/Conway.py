import displayio
import random

class Conways(App):
    def __init__(self, macropad):
        self.macropad = macropad
        self.name = "Conway's GOL"

    def scramble(self, bitmap):
        for x in range(bitmap.width):
            for y in range(bitmap.height):
                bitmap[x, y] = random.randint(0,1)

    def updateGrid(self, old, new): ##creates new grid according to rules of conways game of life
        # code taken from adafruit
        width = old.width 
        height = old.height
        for y in range(height):
            yyy = y * width
            ym1 = ((y + height - 1) % height) * width
            yp1 = ((y + 1) % height) * width
            xm1 = width - 1
            for x in range(width):
                xp1 = (x + 1) % width
                neighbors = (
                    old[xm1 + ym1] + old[xm1 + yyy] + old[xm1 + yp1] +
                    old[x   + ym1] +                  old[x   + yp1] +
                    old[xp1 + ym1] + old[xp1 + yyy] + old[xp1 + yp1])
                new[x+yyy] = neighbors == 3 or (neighbors == 2 and old[x+yyy])
                xm1 = x


    def run(self):
        # displayio.release_displays() #idk what this does
        macropad = self.macropad

        group1 = displayio.Group() # create group
        group2 = displayio.Group()

        bitmap1 = displayio.Bitmap(128, 64, 2)
        bitmap2 = displayio.Bitmap(128, 64, 2)

        palette = displayio.Palette(2) #2 colors
        palette[0] = 0x000000 # set colors for pallete
        palette[1] = 0xFFFFFF

        tiles1 = displayio.TileGrid(bitmap1, pixel_shader=palette) # create tile grid using bitmap and palette
        tiles2 = displayio.TileGrid(bitmap2, pixel_shader=palette)

        group1.append(tiles1) # append tiles to group, to be displayed
        group2.append(tiles2)

        self.scramble(bitmap1)

        while True:
            if macropad.encoder_switch == 1:
                break

            board.DISPLAY.root_group = group1 #set root group
            self.updateGrid(bitmap1, bitmap2)
            board.DISPLAY.root_group = group2 #set root group
            self.updateGrid(bitmap2, bitmap1)