import time
from adafruit_macropad import MacroPad


class Program:
    def __init__(self, macropad):
        self.macropad = macropad
        self.name = "default_program_name"

    def on_press(self, keynumber):
        """called whenever the user has pressed a numpad key. 
        keynumber is from 0 to 11 inclusive"""
        pass

    def on_hold(self, keynumber):
        """called whenever the user is holding a numpad key. 
        keynumber is from 0 to 11 inclusive"""
        pass

    def on_tick(self):
        """called every tick of the program (ie every iteration of the while loop)"""
        pass


class TicTacToe(Program):
    def __init__(self, macropad):
        self.macropad = macropad
        self.name = "tictactoe"


class Simple(Program):
    def __init__(self, macropad):
        self.macropad = macropad
        self.name = "simple"

    def on_press(self, keynumber):
        print("pressed simply")


class Tester(Program):
    def __init__(self, macropad):
        self.macropad = macropad
        self.name = "tester"

    def on_press(self, keynumber):
        print(f"pressed {keynumber}")

    def on_hold(self, keynumber):
        print(f"holding {keynumber}")

    def on_tick(self):
        print("ticked")
        time.sleep(0.5)


class Menu(Program):
    def __init__(self, macropad, programs):
        self.macropad = macropad
        self.name = "menu"
        self.menutext = "hello!"
        self.programs = programs # list of Program's
        self.curr_prgm_idx = 0 # the currently running prgm. idx = 0 when menu is open
        self.prev_prgm_idx = 0 # when menu is open, arrow points here

    def open(self):
        # menu is closed. to open: set arrow idx to point at the prgm that just got hidden
        self.prev_prgm_idx = self.curr_prgm_idx
        self.curr_prgm_idx = 0

    def close(self):
        # menu is opened. to close: go back to previously hidden prgm
        self.curr_prgm_idx = self.prev_prgm_idx
        self.prev_prgm_idx = 0 # menu