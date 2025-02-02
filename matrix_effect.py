import random
import string
import time
class MatrixEffect:
    def __init__(self, window, stop_event):
        self.window = window
        self.stop_event = stop_event
        self.rows = 20
        self.cols = 80
        self.chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    def start(self):
        lines = [" " * self.cols] * self.rows
        self.window["results"].update("\n".join(lines))
        while not self.stop_event.is_set():
            new_line = ''.join(random.choice(self.chars) for _ in range(self.cols))
            lines = [new_line] + lines[:-1]
            self.window["results"].update("\n".join(lines))
            time.sleep(0.1)