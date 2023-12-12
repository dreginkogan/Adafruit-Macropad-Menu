import Apps
import time

class Tester(Apps.App):
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