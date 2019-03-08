from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import time
import datetime
import RPi.GPIO as GPIO
import cv2

class Application(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Basic Time Counter V 0.1 Author Daniel Gee')
##        self.title = 'File Translator'
        self.setGeometry(100,100,230,100)
        self.initGui()

    def initGui(self):
        h1 = QHBoxLayout()
        h2 = QVBoxLayout()

        self.label2 = QLabel(self)
        h2.addWidget(self.label2)
        self.label2.setText('Time elapsed')
        
        self.label1 = QLabel(self)
        f = self.label1.font()
        f.setPointSize(48)
        self.label1.setFont(f)
        
        h2.addWidget(self.label1)

        self.label1.setText('0:00:00.00')

        self.startBtn = QPushButton('Start', self)
        self.startBtn.clicked.connect(self.on_click_start)
        h2.addWidget(self.startBtn)

        self.stopBtn = QPushButton('Stop', self)
        self.stopBtn.clicked.connect(self.on_click_stop)
        h2.addWidget(self.stopBtn)

##        h1.addLayout(h2)

        self.label3 = QLabel(self)
        self.label3.setFixedWidth(320)
        self.label3.setFixedHeight(240)
        self.label3.setFrameShape(QFrame.Box)
        self.label3.setPixmap(QPixmap(r'bkg.png'))

        h2.addWidget(self.label3)
        
        self.setLayout(h2)

        self.timer = QBasicTimer()
        self.t1 = datetime.datetime.now()
##        self.timer.start(100, self)
        
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(7, GPIO.IN)

        self.cap = None



    @pyqtSlot()
    def on_click_start(self):
        ret = GPIO.input(7)
        if ret is 1:
            QMessageBox.warning(self, 'Warning', 'Please Reset sounder catcher!!')
        else:
            self.t1 = datetime.datetime.now()
            self.timer.start(100, self)
            self.startBtn.setEnabled(False)
            self.label3.setPixmap(QPixmap(r'bkg.png'))

            self.cap = cv2.VideoCapture(0)
            if self.cap.isOpened():
                print('Opened a camera')

            else:
                print('Cannot open a camera')
                self.cap = None
            

    @pyqtSlot()
    def on_click_stop(self):
        self.t1 = datetime.datetime.now()
        self.timer.stop()
        self.startBtn.setEnabled(True)

        if self.cap is not None:
                ret = self.cap.grab()
                if ret:
                    flag, frame = self.cap.retrieve()
                    frame = cv2.resize(frame, (320, 240))
                    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    img = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)
                    self.label3.setPixmap(QPixmap.fromImage(img))

                    self.cap.release()


    def timerEvent(self, event):

        t = datetime.datetime.now() - self.t1
        string = '{}'.format(t)
        self.label1.setText(string[:10])

        ret = GPIO.input(7)
        if ret is 1:
            self.timer.stop()
            time.sleep(0.2)
            ret = GPIO.input(7)
            if ret is 1:
                self.startBtn.setEnabled(True)
                if self.cap is not None:
                    ret = self.cap.grab()
                    if ret:
                        flag, frame = self.cap.retrieve()
                        frame = cv2.resize(frame, (320, 240))
                        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        img = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)
                        self.label3.setPixmap(QPixmap.fromImage(img))

                        self.cap.release()
            else:
                self.timer.start(100, self)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Application()
    ex.show()
    sys.exit(app.exec_())
