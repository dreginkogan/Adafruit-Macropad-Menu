import displayio
import random
import board
import Apps
import math
import bitmaptools

import time

def sin(angle):
        return round(math.sin(math.radians(angle)), 3)

def cos(angle):
        return round(math.cos(math.radians(angle)), 3)

def angle(pointX, pointY, centerX, centerY):
    if pointX-centerX == 0:
        if pointY-centerY < 0:
            return -90
        else:
            return 90

    estim = abs(round(math.degrees(math.atan((pointY-centerY)/(pointX-centerX))), 3))

    if pointX-centerX < 0 and pointY-centerY<0: # really stupid and bad code, do not do this
        estim = estim + 180

    if pointX-centerX > 0 and pointY-centerY<0:
        estim = - estim

    if pointX-centerX < 0 and pointY-centerY>0:
        estim = 180 - estim

    if pointX-centerX < 0 and pointY-centerY==0:
        estim = 180 

    return estim

class CycloidalSim(Apps.App):
    def __init__(self, macropad):
        self.macropad = macropad
        self.name = "cycloidal sim"

    def pixelize(self, pointList, width, height): #point list is [ [x, y], ... ]
        pointList[:] = [ [round(i[0]), round(i[1])] for i in pointList]
        # list comprehension/slicing id
        pointList[:] = [j for j in pointList if not (j[0]<0 or j[1]<0 or j[0]>width-1 or j[1]>height-1)]

    def createPath(self, circlePinRadius, eccentricity, reduction, centerX, centerY):

        pointList = []

        for i in range(361):
            j = i*(reduction+1) # roll angle
            pointList.append([centerX + cos(i)*circlePinRadius + cos(j)*eccentricity, centerY + sin(i)*circlePinRadius+ sin(j)*eccentricity])

        # print(pointList)
        return pointList

    def pinOffset(self, pointList, pinRadius, centerX, centerY):
        pointList[:] = [ [ i[0]-cos(angle(i[0],i[1],centerX,centerY))*pinRadius , i[1]-sin(angle(i[0],i[1],centerX,centerY))*pinRadius ] for i in pointList]

    def addHoles(self, bitmap, loadPinRadius, eccentricity, numLoad, centerX, centerY, distFromCent):
        circleRad = loadPinRadius + eccentricity

        for i in range(numLoad):
            angle = i / numLoad  * 360
            bitmaptools.draw_circle(bitmap, round(centerX + cos(angle)*distFromCent), round(centerY + sin(angle)*distFromCent), round(circleRad),1)

    def holes(self, pointList, loadPinRadius, eccentricity, numLoad, centerX, centerY, distFromCent):
        circleRad = loadPinRadius + eccentricity

        for i in range(numLoad):
            angle = i / numLoad  * 360
            for j in range(0, 361, 12):
                pointList.append([centerX + cos(angle)*distFromCent + cos(j)*circleRad, centerY + sin(angle)*distFromCent + sin(j)*circleRad])

    def inToNum(self, macropad): # if no input, the default value will be used instead
        returnNum = ""
        done = False

        while not done:
            key_event = macropad.keys.events.get()

            if key_event:
                if key_event.pressed:
                    if key_event.key_number == 11:
                        break
                    elif key_event.key_number == 0:
                        returnNum += "1"
                    elif key_event.key_number == 1:
                        returnNum += "2"
                    elif key_event.key_number == 2:
                        returnNum += "3"
                    elif key_event.key_number == 3:
                        returnNum += "4"
                    elif key_event.key_number == 4:
                        returnNum += "5"
                    elif key_event.key_number == 5:
                        returnNum += "6"
                    elif key_event.key_number == 6:
                        returnNum += "7"
                    elif key_event.key_number == 7:
                        returnNum += "8"
                    elif key_event.key_number == 8:
                        returnNum += "9"
                    elif key_event.key_number == 9:
                        returnNum += "."
                    elif key_event.key_number == 10:
                        returnNum += "0"
        
        if len(returnNum) == 0:
            return -1

        return float(returnNum) 

    def run(self):
        # pointList = [[0.2, 0.57], [37.37, 48.98], [128, 64], [129, 65], [87, 42.7]] # tests

        # initialize display stuff 
        macropad = self.macropad

        group1 = displayio.Group() # create group

        bitmap1 = displayio.Bitmap(128, 64, 2)

        palette = displayio.Palette(2) #2 colors
        palette[0] = 0x000000 # set colors for pallete
        palette[1] = 0xFFFFFF

        tiles1 = displayio.TileGrid(bitmap1, pixel_shader=palette) # create tile grid using bitmap and palette

        group1.append(tiles1) # append tiles to group, to be displayed
        # ========================

        # variables, make a way to prompt for these for input using numpad

        circlePinRadius = 28 # in pixels
        pinRadius = 5
        eccentricity = 1
        reduction = 14
        loadPinRadius = 3
        numLoad = 5
        loadDist = 12

        # =======================

        # get input

        text_lines = macropad.display_text(title="Enter Parameters")
        text_lines.show()
        
        text_lines[0].text = "Cir pin radius: "
        arg = self.inToNum(macropad) 

        if arg != -1:
            circlePinRadius = arg
 
        text_lines[0].text = "Cir pin radius: " + str(circlePinRadius)

        time.sleep(0.3)

        # =======

        text_lines[0].text = "pin radius: "
        arg = self.inToNum(macropad) 

        if arg != -1:
            pinRadius = arg
 
        text_lines[0].text = "Cir pin radius: " + str(pinRadius)

        time.sleep(0.3)

        # =======

        text_lines[0].text = "eccentricity: "
        arg = self.inToNum(macropad) 

        if arg != -1:
            eccentricity = arg
 
        text_lines[0].text = "eccentricity: " + str(eccentricity)

        time.sleep(0.3)

        











        # =============

        pointList = self.createPath(circlePinRadius, eccentricity, reduction, 63, 31)

        self.pinOffset(pointList, pinRadius, 63, 31 )

        board.DISPLAY.root_group = group1

        # self.addHoles(bitmap1, loadPinRadius, eccentricity, 5, 63, 31, 12)
        self.holes(pointList, loadPinRadius, eccentricity, numLoad, 63, 31, loadDist)

        self.pixelize(pointList, 128, 64)

        for i in pointList:
            bitmap1[i[0], i[1]] = 1
            time.sleep(0.005)


        while True:
            if macropad.encoder_switch == 1:
                break