import displayio
import board
import Apps
import time
import random # random food location

## instead of 1 pixel graphics, do 2x2 pixel tiles, so the food can look different

class Snake(Apps.App):
    def __init__(self, macropad):
        self.macropad = macropad
        self.name = "Snake"

    def foodLoc(self, snakeArr):
        foundUnique = False

        while not foundUnique:
            spawnLoc = [randint(0,63), randint(0,31)]

            for i in snakeArr:
                if spawnLoc != i:
                    foundUnique = True
                    break

        return spawnLoc

    def moveSnake(self, snakeArr, tilegrid, dir):
        pass

    def showSnake(self, turnArr, currPos, startPos, length, tileGrid): # length = int
        drawArr = []
        drawArr.append(currPos)
        if turnArr != []:
            drawArr.append(turnArr)
        drawArr.append(startPos)

        # totalCount = length
        # drawArr = currPos].append(turnArr)
        # draw
        print(drawArr)

        return


    def run(self):
        macropad = self.macropad

        gameBoard = [[0 for x in range(64)] for y in range(32)]

        # setup for display

        group = displayio.Group() # create group

        bitmap = displayio.Bitmap(128, 64, 2)
        bitmap[2,0] = 1
        bitmap[3,0] = 1
        bitmap[2,1] = 1
        bitmap[3,1] = 1
        # bitmap = displayio.OnDiskBitmap('/snakeSource.bmp')

        palette = displayio.Palette(2) #2 colors
        palette[0] = 0x000000 # set colors for pallete
        palette[1] = 0xFFFFFF

        tiles = displayio.TileGrid(bitmap, pixel_shader=palette, width=64, height=32, tile_width=2, tile_height=2, default_tile=0) # create tile grid using bitmap and palette

        group.append(tiles) # append tiles to group, to be displayed

        board.DISPLAY.root_group = group # actually display the shit

        currPos = [32, 16]
        startPos = currPos.copy()

        snakeArr = [[currPos[0], currPos[1]]] # put initial location into the snake array
        bendArr = []

        snakeDir = 0

        while True:
            if macropad.encoder_switch == 1:
                break

            key_event = macropad.keys.events.get()

            oldPos  = currPos

            if key_event:
                if key_event.pressed:
                    bendArr.insert(0, currPos.copy())
                    if key_event.key_number == 1:
                        snakeDir = 0
                        print("up")
                    if key_event.key_number == 3:
                        snakeDir = 3
                        print("left")
                    if key_event.key_number == 4:
                        snakeDir = 2
                        print("down")
                    if key_event.key_number == 5:
                        snakeDir = 1
                        print("right")

            if snakeDir == 0:
                currPos[1] = currPos[1]-1
            elif snakeDir == 1:
                currPos[0] = currPos[0]+1
            elif snakeDir == 2:
                currPos[1] = currPos[1]+1
            else:
                currPos[0] = currPos[0]-1

            if currPos[0]<0 or currPos[0]>63 or currPos[1]<0 or currPos[1]>31:
                break 

        
            if not currPos == oldPos: # currently does the drawing for length 1
                tiles[currPos[0], currPos[1]] = 1
                tiles[oldPos[0], oldPos[1]] = 0

            self.showSnake(bendArr, currPos, startPos, 1, tiles)
            time.sleep(0.2)
            # print(bendArr)



            

                
