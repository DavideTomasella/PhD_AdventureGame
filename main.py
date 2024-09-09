from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5 import QtGui, uic
from game import Game
from text_producer import TextProducer
import os, sys

def resource(relative_path):
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class MainUI(QMainWindow):
    def __init__(self):
        super(QMainWindow,self).__init__()
        uic.loadUi(resource('./resources/main.ui'), self)#background-image:url(resources/bkg_1_small.jpg)
        self.setWindowIcon(QtGui.QIcon(resource("./resources/icon.ico").replace("\\","/")))
        self.setStyleSheet("background-image:url(\""+resource("resources/bkg_1_small.jpg").replace("\\","/")+"\");")
        self.connectEvents()

        self.show()
        self.game = Game()
        self.start_game_and_update_gui()

    def connectEvents(self):
        self.btn_false.clicked.connect(self.onClk_false)
        self.btn_true.clicked.connect(self.onClk_true)
        self.textAreaProducer = TextProducer(self.textArea)
        self.textAreaProducer.letterChanged.connect(self.textArea.insertPlainText)
        self.textAreaProducer.clearText.connect(self.textArea.clear)

    def loadUI(self):
        self.btn_false = QPushButton("False", self)
        self.btn_true = QPushButton("True", self)
        self.textArea = QTextEdit(self)

    def start_game_and_update_gui(self):
        if self.game.is_running:
            self.btn_false.setText("Reschedule task")
            self.btn_true.setText("Accept task")
        else:
            self.textAreaProducer.text = self.game.start_game()
            self.btn_false.setText("Don't start the game")
            self.btn_true.setText("Start the game")

    def stop_game_and_update_gui(self):
        if not self.game.is_running:
            self.btn_false.setText("Celebrate!")
            self.btn_true.setText("Celebrate!")

    def onClk_false(self):
        self.start_game_and_update_gui()
        self.textAreaProducer.text = self.game.advance_game(1)
        self.stop_game_and_update_gui()

    def onClk_true(self):
        self.start_game_and_update_gui()
        self.textAreaProducer.text = self.game.advance_game(2)
        self.stop_game_and_update_gui()

#if __name__ == '__main__':
app = QApplication([])
window = MainUI()
app.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
app.exec()
