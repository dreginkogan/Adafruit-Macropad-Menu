import time
from adafruit_macropad import MacroPad

from rainbowio import colorwheel
from adafruit_macropad import MacroPad

import board


class App:
    def __init__(self, macropad):
        self.macropad = macropad
        self.name = "default_program_name"

    def run(self):
        pass

class Conway(App):
    def __init__(self, macropad):
        self.macropad = macropad
        self.name = "Conway"

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


class Snake(App):
    def __init__(self, macropad):
        self.macropad = macropad
        self.name = "snake"

    def run(self):
        print("also also does nothing rn")

class imgTest(App): #this must be figured out
    def __init__(self, macropad):
        self.macropad = macropad
        self.name = "Image Test"

    def run(self):
        macropad = self.macropad

        splash = displayio.Group() # create group

        #####

        bitmap = displayio.Bitmap(128, 64, 2) #set bitmap size and number of colors
        palette = displayio.Palette(2) #2 colors

        palette[0] = 0x000000 # set colors for pallete
        palette[1] = 0xFFFFFF

        tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette) # create tile grid using bitmap and palette
        splash.append(tile_grid) # tiles 

        board.DISPLAY.root_group = splash #set root group

        while True:
            if macropad.encoder_switch == 1:
                break

            bitmap.fill(1)
            time.sleep(0.25)
            bitmap.fill(0)
            time.sleep(0.25)

class aScale(App):
    def __init__(self, macropad):
        self.macropad = macropad
        self.name = "A Scale"

    def run(self):
        tones = [831, 880, 932, 988, 1047, 1109, 1175, 1245, 1319, 1397, 1480, 1568]
        macropad = self.macropad

        while True:
            if macropad.encoder_switch == 1:
                # for i in range(12):
                #      macropad.pixels[i] = colorwheel(0) # turns lights off
                break

            key_event = macropad.keys.events.get()

            keyLight = 100

            # macropad.pixels[0] = colorwheel(int(keyLight))
            # macropad.pixels[2] = colorwheel(int(keyLight))
            # macropad.pixels[3] = colorwheel(int(keyLight))
            # macropad.pixels[6] = colorwheel(int(keyLight))
            # macropad.pixels[7] = colorwheel(int(keyLight))
            # macropad.pixels[9] = colorwheel(int(keyLight))
            # macropad.pixels[10] = colorwheel(int(keyLight))

            if key_event:
                if key_event.pressed:
                    # macropad.pixels[key_event.key_number] = colorwheel(int(255/12) * key_event.key_number)
                    macropad.start_tone(tones[key_event.key_number])

                else:
                    macropad.pixels.fill((0, 0, 0))
                    macropad.stop_tone()

class TicTacToe(App):
    def __init__(self, macropad):
        self.macropad = macropad
        self.name = "tictactoe"

    def print_board(self, backend):
        macropad = self.macropad
        text_lines = macropad.display_text(title="==== Tic Tac Toe ====")

        BOARD_DICT = {
            -1: "-",
            0: "X",
            1: "O",
        }

        for i in range(3):
            text_lines[i+1].text = "         " + BOARD_DICT[backend[i][0]] + BOARD_DICT[backend[i][1]] + BOARD_DICT[backend[i][2]]

        text_lines.show()

    def run(self):

        macropad = self.macropad

        curr_board = [
            [-1, -1, -1],
            [-1, -1, -1],
            [-1, -1, -1],
        ]

        self.print_board(curr_board)

        curr_player = 0  # translate via BOARD_DICT
        button_held = False

        while True:
            if macropad.encoder_switch == 1:
                break

            key_event = macropad.keys.events.get()
            if key_event:
                if key_event.pressed:
                    if not button_held:
                        button_held = True
                        user_input: int = key_event.key_number # 0 to 11 inclusive

                        if user_input == 11: # quit
                            print("joe mama")

                        elif user_input == 10: # redo
                            curr_board = [
                                [-1, -1, -1],
                                [-1, -1, -1],
                                [-1, -1, -1],
                            ]
                            curr_player = 0
                            self.print_board(curr_board)
                            continue

                        elif 0 <= user_input < 9:
                            row = user_input // 3
                            col = user_input % 3

                            curr_board[row][col] = curr_player
                            self.print_board(curr_board)

                            curr_player = 1 if curr_player == 0 else 0

                        else:
                            continue

                    else: # if button is held,
                        pass # do nothing
                else: # no key is pressed
                    button_held = False

class Sussy(App):
    def __init__(self, macropad):
        self.macropad = macropad
        self.name = "sussy"

    def run(self):
        macropad = self.macropad

        macropad.display_image("sussy.bmp")

        poo = True
        oldPoo = poo

        while True:
            if macropad.encoder_switch == 1:
                break

            key_event = macropad.keys.events.get()
            if key_event and key_event.pressed and key_event.key_number == 0:
                oldPoo = poo
                poo = not poo
                print("amog")
                print(poo)

            if poo != oldPoo:
                if poo:
                    macropad.display_image("sussy.bmp")
                    print("your mame")
                else:
                    macropad.display_image("blinka.bmp")
                    print("cindy is a meow meow")
            oldPoo = poo
            time.sleep(0.1)
