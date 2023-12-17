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
