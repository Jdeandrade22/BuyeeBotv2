import random
import time

class MatrixEffect:
    def __init__(self, window, stop_event):
        self.window = window
        self.stop_event = stop_event

    def start(self):
        matrix_chars = "01"
        while not self.stop_event.is_set():
            matrix_line = ''.join(random.choice(matrix_chars) for _ in range(80))
            try:
                self.window["results"].update(matrix_line + '\n', append=True)
                time.sleep(0.1)
            except:
                break