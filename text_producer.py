from PyQt5.QtCore import QTimer, QObject, pyqtSignal
import random

class TextProducer(QObject):
    letterChanged = pyqtSignal(str)
    clearText = pyqtSignal()

    def __init__(self, parent=None):
        super(TextProducer, self).__init__(parent)
        self._text = ""
        self._text_it = None
        self._timer = QTimer(self, timeout=self._handle_timeout)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
        self.start(interval=int(random.gauss(30,5)))

    def start(self, interval : int = 1000):
        self.clearText.emit()
        self._text_it = iter(self.text)
        self._timer.start(interval)
        #self._handle_timeout()

    def stop(self):
        self._timer.stop()
        self._text_it = None

    def _handle_timeout(self):
        try:
            letter = next(self._text_it)
        except StopIteration as e:
            self._timer.stop()
        else:
            self.letterChanged.emit(letter)

