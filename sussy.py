# A really stupid test file

import time
from adafruit_macropad import MacroPad

macropad = MacroPad()

macropad.display_image("sussy.bmp")

poo = True
oldPoo = poo

while True:
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
