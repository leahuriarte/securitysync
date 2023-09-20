from audio import *
from video import *
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,QMainWindow
from PyQt5.QtGui import QPalette, QColor, QPixmap
from PyQt5.QtCore import *
from pathlib import Path
import sys

#retrieve audio and video input for real time analysis
def input(window):
    hate_language = []
    audio = threading.Thread(target=runAudio, args=(hate_language,))
    audio.start()
    tired_count = recordVideo(window)
    #audio.join()
    window.finalScreen(hate_language, tired_count)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        #set window attributes
        self.setWindowTitle("Security Sync")
        self.setObjectName("background")
        self.setFixedSize(720,900)

        #create main widget
        mainWidget = self.mainCentralWidget()
        self.setCentralWidget(mainWidget)
        self.show()

    #creating home screen
    def mainCentralWidget(self):
        #create layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        #create title
        self.title = QLabel("Security Sync")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFixedHeight(100)
        layout.addWidget(self.title)

        #create image
        self.image = QLabel()
        self.image.setPixmap(QPixmap("main.png").scaled( 450 , 450 , Qt.KeepAspectRatio))
        self.image.setFixedHeight(400)
        self.image.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image)

        #create button
        self.button = QPushButton("Start Ride")
        self.button.setFixedSize(500,70)
        self.button.clicked.connect(self.handleButton)
        self.button.setToolTip("Start Ride")
        layout.addWidget(self.button)

        mainWidget = QWidget()
        mainWidget.setLayout(layout)

        return mainWidget
    
    #status screen giving real time updates on fatigue
    def recordCentralWidget(self, text):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        self.car_image = QLabel()
        self.car_image.setPixmap(QPixmap("car.png").scaled( 200, 200, Qt.KeepAspectRatio))
        layout.addWidget(self.car_image)
        
        self.statusTitle = QLabel("Status")
        layout.addWidget(self.statusTitle)
        self.status = QLabel(text)
        self.status.setObjectName("status")
        layout.addWidget(self.status)

        mainWidget = QWidget()
        mainWidget.setLayout(layout)

        return mainWidget

    #when button clicked
    def handleButton(self):
        self.update("")
        input(self)

    #update screen
    def update(self, text):
        mainWidget = self.recordCentralWidget(text)
        self.setCentralWidget(mainWidget)
        self.show()

    #summary screen with statistics
    def finalScreen(self, hate, tired):
        #create layout
        layout2 = QVBoxLayout()
        layout2.setAlignment(Qt.AlignCenter)

        #create title
        self.title2 = QLabel("Hate Speech")
        layout2.addWidget(self.title2)

        #report hate speech instances
        #if none
        if (len(hate) == 0):
            self.hate = QLabel("No hate speech was detected")
            self.hate.setObjectName("hate")
            layout2.addWidget(self.hate)

        #otherwise add each instance
        else:
            layout2.addWidget(QLabel("Investigate these incidents"))
            for text in hate:
                self.hate = QLabel('"' + text + '"')
                self.hate.setObjectName("hate")
                layout2.addWidget(self.hate)

        #report fatigue as a percent
        tired_percent = round((tired/214)*100)
        self.tired = QLabel(str(tired_percent) + "% fatigue level")
        layout2.addWidget(self.tired)
        #alert Uber to check in on driver if high fatigue
        if (tired_percent >= 20):
            self.contact = QLabel("Contact driver to ensure safety")
            self.contact.setObjectName("contact")
            layout2.addWidget(self.contact)

        #update screen with new widgets
        finalWidget = QWidget()
        finalWidget.setLayout(layout2)

        self.setCentralWidget(finalWidget)
        self.show()

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(Path('style.qss').read_text())
    window = MainWindow()
    sys.exit(app.exec_())