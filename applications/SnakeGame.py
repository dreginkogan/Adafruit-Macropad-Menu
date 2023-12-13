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


    def showSnake(self, drawArr, length, tileGrid): # length = int

        drawColor = 1
        count = 1

        print(f"sussy amogus {drawArr}")

        if len(drawArr)>length+1:
            del drawArr[length+1:]


        for i in range(len(drawArr)-1):
            startPoint = drawArr[i]
            endPoint = drawArr[i+1]

            tempLoc = startPoint.copy()

            difX = drawArr[i+1][0]-drawArr[i][0]
            difY = drawArr[i+1][1]-drawArr[i][1]

            while tempLoc != endPoint: # if it gets to drawing the end point, stop
                if count>length and drawColor != 0: # maybe turning the frown upside down will help?
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

                # if tileGrid[tempLoc[0], tempLoc[1]] != drawColor: #maybe this will stop the tweaking???
                tileGrid[tempLoc[0], tempLoc[1]] = drawColor # it did not fix it

                # the flickering does not happen when all the squares would be drawn white
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

        # snakeArr = [[currPos[0], currPos[1]]] # put initial location into the snake array
        bendArr = [currPos.copy()]
        bendArr.append(startPos)


        snakeDir = 0

        snakeLength = 17;

        while True:
            if macropad.encoder_switch == 1:
                break

            key_event = macropad.keys.events.get()

            oldPos  = currPos.copy()

            bendArr[0] = currPos.copy()

            if key_event:
                if key_event.pressed:
                    bendArr.insert(1, currPos.copy())
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

            print(bendArr)

        
            # if not currPos == oldPos: # currently does the drawing for length 1
            #     tiles[currPos[0], currPos[1]] = 1
            #     tiles[oldPos[0], oldPos[1]] = 0

            self.showSnake(bendArr, 3, tiles)
            time.sleep(0.05)
            # print(currPos)



            

                
