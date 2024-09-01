from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit
from PyQt5 import QtGui, uic
from game import Game
from text_producer import TextProducer

class MainUI(QMainWindow):
    def __init__(self):
        super(QMainWindow,self).__init__()
        self.game = Game()
        uic.loadUi('./main.ui', self)
        self.setWindowIcon(QtGui.QIcon("./resources/icon.png"))
        self.connectEvents()

        self.show()
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

if __name__ == '__main__':
    app = QApplication([])
    window = MainUI()
    exit(app.exec_())
