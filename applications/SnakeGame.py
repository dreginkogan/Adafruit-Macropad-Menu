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


    def showSnake(self, turnArr, currPos, startPos, length, tileGrid): # length = int
        drawArr = []
        drawArr.append(currPos.copy())
        if turnArr != []:
            drawArr.extend(turnArr) # extend adds elements of an array to another list, instead of just adding a whole array to the end
        drawArr.append(startPos)

        drawColor = 1
        count = 1

        # implement anti flickering algorithm
        # if amount of elemets already shwon in new array, dont bother resetting them, only set new ones
        # the snake is tweaking so hard

        # maybe only worry about updating the first and last segments?

        for i in range(len(drawArr)-1):
            startPoint = drawArr[i]
            endPoint = drawArr[i+1]

            tempLoc = startPoint.copy()

            difX = drawArr[i+1][0]-drawArr[i][0]
            difY = drawArr[i+1][1]-drawArr[i][1]

            while tempLoc != endPoint: # if it gets to drawing the end point, stop
                if (count>length):
                    drawColor = 0
                    # print(tempLoc)

                if difX<0:
                    tempLoc[0] = tempLoc[0] - 1
                elif difX>0:
                    tempLoc[0] = tempLoc[0] + 1

                if difY<0:
                    tempLoc[1] = tempLoc[1] - 1
                elif difY>0:
                    tempLoc[1] = tempLoc[1] + 1

                tileGrid[tempLoc[0], tempLoc[1]] = drawColor

                count = count + 1
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

        bitmap[4,0] = 1
        bitmap[5,1] = 1
        bitmap[6,1] = 1
        bitmap[7,0] = 1
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
                    if key_event.key_number == 1 and snakeDir != 2:
                        snakeDir = 0
                        print("up")
                    if key_event.key_number == 3 and snakeDir != 1:
                        snakeDir = 3
                        print("left")
                    if key_event.key_number == 4 and snakeDir != 0:
                        snakeDir = 2
                        print("down")
                    if key_event.key_number == 5 and snakeDir != 3:
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
                time.sleep(.25)
                break 

        
