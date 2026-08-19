import sys
import json
import os
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,QWidget
from PySide6.QtCore import Slot, Qt
from pynput import keyboard


class Overlay:
    def __init__(self, owner):
        self.BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
        self.DATA_PATH = os.path.join(self.BASE_DIR, "data.json")
        if not os.path.exists(self.DATA_PATH):
            default_data = {"prev": "f8", "next": "f9", "reop": "f6"}
            with open(self.DATA_PATH, "w") as file:
                json.dump(default_data, file, indent=4)

        with open(self.DATA_PATH, "r") as file: 
            self.data = json.load(file)
        self.owner = owner
        self.app = QApplication.instance() or QApplication([])
        self.window = QWidget()
        self.window.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.window.setAttribute(Qt.WA_TranslucentBackground)
        self.lay = QVBoxLayout(self.window)
        self.top = QHBoxLayout()
        self.button = QPushButton("k")
        self.button.clicked.connect(self.beh)
        self.button.setFixedSize(40, 40)
        self.button.setStyleSheet("""
            QPushButton {
                background: #181818;
                color: white;
                border: none;
                border-radius: 21px;
                font-size: 19px;
            }

            QPushButton:hover {
                background: #282828;
            }

            QPushButton:pressed {
                background: #383838;
            }
        """)
        self.top.addStretch(16)
        self.top.addWidget(self.button)
        self.top.addStretch(188)
        self.lay.addStretch(1)
        self.lay.addLayout(self.top)
        self.lay.addStretch(56)      
        self.window.resize(500, 100)
        self.window.show()
    
    @Slot()
    def beh(self):
        self.smallWind = QWidget(self.window)
        self.smallWind.resize(self.window.width() // 9, self.window.height() // 9)
        self.mainLay = QVBoxLayout(self.smallWind)
        self.rowP = QHBoxLayout()
        self.label = QLabel()
        self.label.setText("key bind for previos: " + self.data["prev"])
        self.setterP = QPushButton()
        self.setterP.setText("set")
        self.setterP.clicked.connect(self.setP)
        self.setterP.setFixedSize(40, 40)
        self.rowP.addWidget(self.label)
        self.rowP.addWidget(self.setterP)
        self.rowN = QHBoxLayout()
        self.labelN = QLabel()
        self.labelN.setText("key bind for Next: " + self.data["next"])
        self.setterN = QPushButton()
        self.setterN.setText("set")
        self.setterN.clicked.connect(self.setN)
        self.setterN.setFixedSize(40, 40)
        self.rowN.addWidget(self.labelN)
        self.rowN.addWidget(self.setterN)
        self.rowO = QHBoxLayout()
        self.labelO = QLabel()
        self.labelO.setText("key bind for reopen: " + self.data["reop"])
        self.setterO = QPushButton()
        self.setterO.setText("set")
        self.setterO.clicked.connect(self.setO)
        self.setterO.setFixedSize(40, 40)
        self.rowO.addWidget(self.labelO)
        self.rowO.addWidget(self.setterO)
        self.mainLay.addLayout(self.rowP)
        self.mainLay.addLayout(self.rowN)
        self.mainLay.addLayout(self.rowO)
        self.smallWind.setWindowFlags(Qt.Window)
        self.smallWind.setAttribute(Qt.WA_TranslucentBackground, False)
        self.smallWind.setWindowTitle("key binding")
        self.smallWind.show()
        

    @Slot()
    def setP(self):
        def on_press(key):
            try:
                captured_key = key.char
            except AttributeError:
                captured_key = key.name

            if captured_key:
                self.data["prev"] = captured_key
                with open("data.json", "w") as file:
                    json.dump(self.data, file, indent=4)
                self.label.setText("key bind for previos: " + str(self.data["prev"]))
                self.owner.restartKey()

            return False

        listener = keyboard.Listener(on_press=on_press)
        listener.start()

    @Slot()
    def setN(self):
        def on_press(key):
            try:
                captured_key = key.char
            except AttributeError:
                captured_key = key.name

            if captured_key:
                self.data["next"] = captured_key
                with open("data.json", "w") as file:
                    json.dump(self.data, file, indent=4)
                self.labelN.setText("key bind for next: " + str(self.data["next"]))
                self.owner.restartKey()

            return False

        listener = keyboard.Listener(on_press=on_press)
        listener.start()

    @Slot()
    def setO(self):
        def on_press(key):
            try:
                captured_key = key.char
            except AttributeError:
                captured_key = key.name

            if captured_key:
                self.data["reop"] = captured_key
                with open("data.json", "w") as file:
                    json.dump(self.data, file, indent=4)
                self.labelO.setText("key bind for reopen: " + str(self.data["reop"]))
                self.owner.restartKey()

            return False

        listener = keyboard.Listener(on_press=on_press)
        listener.start()

    def GUI(self):
        return self.window

    def resizeOrMoveOrVisible(self,window,a,b,c,d,vis):
        window.setGeometry(c,d,a,b)
        window.setVisible(vis)

    def run(self):
        self.app.exec()

    def end(self):
        self.app.quit()
if __name__ == "__main__":
    Overlay.GUI()