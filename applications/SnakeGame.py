import displayio
import board
import Apps
import time
import random # random food location
import adafruit_imageload

## instead of 1 pixel graphics, do 2x2 pixel tiles, so the food can look different

class Snake(Apps.App):
    def __init__(self, macropad):
        self.macropad = macropad
        self.name = "Snake"

    def foodLoc(self, snakeArr):
        foundUnique = False
        spawnLoc = [0,0]

        while not foundUnique:
            spawnLoc = [random.randint(0,31), random.randint(0,15)]

            for i in snakeArr:
                if spawnLoc != i:
                    foundUnique = True
                    break

        return spawnLoc

    def snakeFoodCollision(self, headPos, food):
        if headPos == food:
            return True
        else:
            return False

    def snakeSnakeCollision(self, snakeArr):
        for j in range(1, len(snakeArr)):
            if snakeArr[0] == snakeArr[j]:
                return True
        
        return False

    def showSnake(self, drawArr, darkArr, tileGrid): # length = int

        for j in darkArr:
            tileGrid[j[0], j[1]] = 0
        
        for i in drawArr:
            tileGrid[i[0], i[1]] = 1 # something is causing an index error here

        return


    def run(self):
        macropad = self.macropad

        # setup for display

        group = displayio.Group() # create group

        palette = displayio.Palette(2) #2 colors
        palette[0] = 0x000000 # set colors for pallete
        palette[1] = 0xFFFFFF

        bitmap, palette = adafruit_imageload.load("/snakeSource.bmp",
                                          bitmap=displayio.Bitmap(128, 64, 2),
                                          palette=palette)


        tiles = displayio.TileGrid(bitmap, pixel_shader=palette, width=32, height=16, tile_width=4, tile_height=4, default_tile=0) # create tile grid using bitmap and palette

        group.append(tiles) # append tiles to group, to be displayed

        board.DISPLAY.root_group = group # actually display the shit

        currPos = [16, 8]

        # snakeArr = [[currPos[0], currPos[1]]] # put initial location into the snake array
        bendArr = [currPos.copy(), [16, 9], [16, 10], [16, 11], [16, 12]]

        snakeDir = [0, -1]

        snakeLength = 5
        foodPos = self.foodLoc(bendArr)
        # print(f"initial food location is {foodPos}")

        foodState = False # for animation

        while True:
            if macropad.encoder_switch == 1:
                break

            key_event = macropad.keys.events.get()

            if key_event:
                if key_event.pressed:
                    # bendArr.insert(1, currPos.copy())
                    if key_event.key_number == 1 and snakeDir[1] != 1:
                        snakeDir = [0, -1]
                        # print("up")
                    if key_event.key_number == 3 and snakeDir[0] != 1:
                        snakeDir = [-1, 0]
                        # print("left")
                    if key_event.key_number == 4 and snakeDir[1] != -1:
                        snakeDir = [0, 1]
                        # print("down")
                    if key_event.key_number == 5 and snakeDir[0] != -1:
                        snakeDir = [1, 0]
                        # print("right")
                    if key_event.key_number == 10:
                        snakeLength = snakeLength + 10
                        # print("more")

            currPos[0] = currPos[0]+snakeDir[0]
            currPos[1] = currPos[1]+snakeDir[1]

            if currPos[0]<0 or currPos[0]>31 or currPos[1]<0 or currPos[1]>15:
                time.sleep(.5)
                break 
            
            # print(f"curr pos = {currPos}")
            bendArr.insert(0, currPos.copy())
            darkArr = bendArr[snakeLength:snakeLength+2] # +1 leaves little poops everywhere
            bendArr = bendArr[:snakeLength]
            # print(f"bendArr = {bendArr}")

            self.showSnake(bendArr, darkArr, tiles)

            if foodState:
                tiles[foodPos[0], foodPos[1]] = 2
                foodState = False
            else:
                tiles[foodPos[0], foodPos[1]] = 3
                foodState = True

            if self.snakeFoodCollision(currPos, foodPos):
                snakeLength = snakeLength + 5
                foodPos = self.foodLoc(bendArr)

            if self.snakeSnakeCollision(bendArr):
                time.sleep(.5)
                break 
            
            time.sleep(0.06)
            # print(currPos)