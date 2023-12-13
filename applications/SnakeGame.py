import displayio
import board
import Apps

## instead of 1 pixel graphics, do 2x2 pixel tiles, so the food can look different

class Snake(Apps.App):
    def __init__(self, macropad):
        self.macropad = macropad
        self.name = "Snake"

    def run(self):
        macropad = self.macropad

        gameBoard = [[0 for x in range(64)] for y in range(32)]
        currPos = [32, 16]

        # setup for display

        group = displayio.Group() # create group

        bitmap = displayio.Bitmap(128, 64, 2)

        palette = displayio.Palette(2) #2 colors
        palette[0] = 0x000000 # set colors for pallete
        palette[1] = 0xFFFFFF

        tiles = displayio.TileGrid(bitmap, palette, 64, 32, 2, 2) # create tile grid using bitmap and palette

        group.append(tiles) # append tiles to group, to be displayed

        while True:
            if macropad.encoder_switch == 1:
                break

            key_event = macropad.keys.events.get()

            oldPos  = currPos

            if key_event:
                if key_event.pressed:
                    if key_event.key_number == 1:
                        currPos = [currPos[0], currPos[1]-1]
                        print("up")
                    if key_event.key_number == 3:
                        currPos = [currPos[0]-1, currPos[1]]
                        print("left")
                    if key_event.key_number == 4:
                        currPos = [currPos[0], currPos[1]+1]
                        print("down")
                    if key_event.key_number == 5:
                        currPos = [currPos[0]+1, currPos[1]]
                        print("right")

            print(currPos)
            gameBoard[oldPos[0], oldPos[1]] = 0
            gameBoard[currPos[0], currPos[1]] = 1

            

                
