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
        spawnLoc = [0,0]

        while not foundUnique:
            spawnLoc = [random.randint(0,63), random.randint(0,31)]

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

    def snakeSnakeCollision(self, headPos, snakeArr):
        for i in snakeArr:
            if snakeArr == headPos:
                return True
        
        return False

    def showSnake(self, drawArr, darkArr, tileGrid): # length = int

        for j in darkArr:
            tileGrid[j[0], j[1]] = 0
        
        for i in drawArr:
            tileGrid[i[0], i[1]] = 1

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

        # snakeArr = [[currPos[0], currPos[1]]] # put initial location into the snake array
        bendArr = [currPos.copy(), [32, 17], [32, 18], [32, 19], [32, 20]]

        snakeDir = [0, -1]

        snakeLength = 5
        foodPos = self.foodLoc(bendArr)
        print(f"initial food location is {foodPos}")

        foodState = False

        while True:
            if macropad.encoder_switch == 1:
                break

            key_event = macropad.keys.events.get()

            if key_event:
                if key_event.pressed:
                    bendArr.insert(1, currPos.copy())
                    if key_event.key_number == 1:
                        snakeDir = [0, -1]
                        # print("up")
                    if key_event.key_number == 3:
                        snakeDir = [-1, 0]
                        # print("left")
                    if key_event.key_number == 4:
                        snakeDir = [0, +1]
                        # print("down")
                    if key_event.key_number == 5:
                        snakeDir = [1, 0]
                        # print("right")
                    if key_event.key_number == 10:
                        snakeLength = snakeLength + 10
                        # print("more")

            currPos[0] = currPos[0]+snakeDir[0]
            currPos[1] = currPos[1]+snakeDir[1]

            if currPos[0]<0 or currPos[0]>63 or currPos[1]<0 or currPos[1]>31:
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
                snakeLength = snakeLength + 15
                foodPos = self.foodLoc(bendArr)

            if self.snakeSnakeCollision(currPos, bendArr):
                time.sleep(.5)
                break 
            
            time.sleep(0.05)
            # print(currPos)