import time
from adafruit_macropad import MacroPad


class App:
    def __init__(self, macropad):
        self.macropad = macropad
        self.name = "default_program_name"

    def run(self):
        pass


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

        print(backend[0][0])

        for i in range(3):
            text_lines[i].text = BOARD_DICT[backend[i][0]] + BOARD_DICT[backend[i][1]] + BOARD_DICT[backend[i][2]]

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


class Snake(App):
    def __init__(self, macropad):
        self.macropad = macropad
        self.name = "snake"

    def run(self):
        print("also also does nothing rn")


class Tester(App):
    def __init__(self, macropad):
        self.macropad = macropad
        self.name = "tester"

    def run(self):
        macropad = self.macropad

        text_lines = macropad.display_text(title="======= test =======")
        text_lines.show()
        text_lines[0].text = "test app"
        text_lines[1].text = "will close"
        text_lines[2].text = "in 2s"
        time.sleep(1)
        text_lines[2].text = "in 1s"
        time.sleep(1)