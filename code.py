import time
import Apps
from adafruit_macropad import MacroPad

macropad = MacroPad()

applications = [
    Apps.TicTacToe(macropad),
    Apps.Sussy(macropad),
    Apps.Snake(macropad),
    Apps.Tester(macropad),
    Apps.aScale(macropad),
    Apps.imgTest(macropad),
]


def getIdx(offset: int) -> int:
    """gets index of application from encoder"""
    return (macropad.encoder + offset) % len(applications)


text_lines = macropad.display_text(title="======= Menu =======")

oldState = 0.5 # placeholder value

while True:

    encoderPosition = macropad.encoder

    if encoderPosition != oldState:
        text_lines[0].text = applications[getIdx(offset=-1)].name
        text_lines[1].text = "> " + applications[getIdx(offset=0)].name
        text_lines[2].text = applications[getIdx(offset=1)].name
        text_lines.show()

    if macropad.encoder_switch == 1:
        text_lines[1].text = " >" + applications[getIdx(offset=0)].name
        time.sleep(0.25)
        applications[getIdx(offset=0)].run()
        text_lines.show()
        time.sleep(0.25)
        text_lines[1].text = "> " + applications[getIdx(offset=0)].name

    oldState = encoderPosition