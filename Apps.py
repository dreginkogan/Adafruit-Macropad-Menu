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

    def run(self):
        print("does nothing rn")


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


class Tester(Program):
    def __init__(self, macropad):
        self.macropad = macropad
        self.name = "tester"

    def run(self):
        text_lines = macropad.display_text(title="======= test =======")
        text_lines[0].text = "test app"
        text_lines[1].text = "will close"
        text_lines[2].text = "in 2s"
        text_lines.show()
        time.sleep(2)
