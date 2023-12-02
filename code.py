import time
import Apps
from adafruit_macropad import MacroPad

macropad = MacroPad()

applications = [
    Apps.TicTacToe(macropad),
    Apps.Sussy(macropad),
    Apps.Snake(macropad),
    Apps.Tester(macropad),
]


def getIdx(offset: int) -> int:
    """gets index of application from encoder"""
    return (macropad.encoder + offset) % len(applications)


text_lines = macropad.display_text(title="======= Menu =======")
text_lines.show()

oldState = -1

while True:

    encoderPosition = macropad.encoder

    if encoderPosition != oldState:
        text_lines[0].text = applications[getIdx(offset=-1)].name
        text_lines[1].text = "> " + applications[getIdx()].name
        text_lines[2].text = applications[getIdx(offset=1)].name

    if macropad.encoder_switch == 1:
        text_lines[1].text = " >" + applications[getIdx()].name
        time.sleep(0.25)
        applications[getIdx()].run()
        text_lines[1].text = "> " + applications[getIdx()].name

    oldState = encoderPosition
