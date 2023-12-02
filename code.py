import time
from adafruit_macropad import MacroPad

macroPad = MacroPad()

applications = ["The",
                "Quick",
                "Brown",
                "idk",
                "hello",
                "goodbye",
                ]

text_lines = macroPad.display_text(title="======= Menu =======")
text_lines.show()

text_lines[0].text = applications[(macroPad.encoder-1) % len(applications)]
text_lines[1].text = "> " + applications[(macroPad.encoder) % len(applications)]
text_lines[2].text = applications[(macroPad.encoder+1) % len(applications)]

# print(applications[(macroPad.encoder-1) % len(applications)])
# print("> " + applications[(macroPad.encoder) % len(applications)])
# print(applications[(macroPad.encoder+1) % len(applications)])

oldState = 0;

while True:

    encoderPosition = macroPad.encoder

    if encoderPosition != oldState:
        text_lines[0].text = applications[(encoderPosition-1) % len(applications)]
        text_lines[1].text = "> " + applications[(encoderPosition) % len(applications)]
        text_lines[2].text = applications[(encoderPosition+1) % len(applications)]

    if macroPad.encoder_switch == 1:
        text_lines[1].text = " >" + applications[(encoderPosition) % len(applications)]
        time.sleep(.25)
        text_lines[1].text = "> " + applications[(encoderPosition) % len(applications)]

    oldState = encoderPosition
    time.sleep(0.1)
