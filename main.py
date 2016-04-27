#!/usr/bin/python

import sys, random, struct, time
from PySide.QtCore import *
from PySide.QtGui import *
from main_ui import Ui_MainWindow

import function

class transProcess(QThread):
    message = Signal(str)

    def __init__(self, num, parent=None):
        super(transProcess,self).__init__(parent)
        self.num = num

    def run(self):
        first_uid, first_sum = rfid.read()
        first_sum = first_sum - self.num
        rfid.write(first_sum)

        self.message.emit('Put another card')

        while True:
            second_uid, second_sum = rfid.read()
            self.msleep(500)
            if not second_uid == first_uid:
                second_sum = second_sum + self.num
                rfid.write(second_sum)
                second_uid, second_sum = rfid.read()
                self.message.emit('{:,}'.format(second_sum))
                return 0


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        
        global rfid
        rfid = function.RFID(4)

        self.operator = ''
        self.clear_flag = True
        self.equGetDisplay_flag = False
        self.num = 0

        self.b0.clicked.connect(lambda: self.insert_num('0'))
        self.b00.clicked.connect(lambda: self.insert_num('00'))
        self.b1.clicked.connect(lambda: self.insert_num('1'))
        self.b2.clicked.connect(lambda: self.insert_num('2'))
        self.b3.clicked.connect(lambda: self.insert_num('3'))
        self.b4.clicked.connect(lambda: self.insert_num('4'))
        self.b5.clicked.connect(lambda: self.insert_num('5'))
        self.b6.clicked.connect(lambda: self.insert_num('6'))
        self.b7.clicked.connect(lambda: self.insert_num('7'))
        self.b8.clicked.connect(lambda: self.insert_num('8'))
        self.b9.clicked.connect(lambda: self.insert_num('9'))

        self.bread.clicked.connect(self.read)
        self.binit.clicked.connect(lambda: self.write(self.display.text()))
        self.btrans.clicked.connect(self.trans)
        self.bcls.clicked.connect(self.cls)
        self.bpls.clicked.connect(self.pls)
        self.bmns.clicked.connect(self.mns)
        self.bequ.clicked.connect(lambda: self.equ(self.display.text()))
        # self.bf2.clicked.connect(self.test)

    def updateText(self,text):
        self.display.clear()
        self.display.insert(text)
        self.clear_flag = True

    def trans(self):
        self.updateThread = transProcess(int(self.display.text().replace(',','')))
        #connect our update functoin to the progress signal of the update thread
        self.updateThread.message.connect(self.updateText,Qt.QueuedConnection)
        if not self.updateThread.isRunning():#if the thread has not been started let's kick it off
            self.updateThread.start()

    def mns(self):
        self.operator = "mns"
        self.clear_flag = True
        self.equGetDisplay_flag = True

    def pls(self):
        self.operator = "pls"
        self.clear_flag = True
        self.equGetDisplay_flag = True

    def cls(self):
        self.display.clear()
        self.display.insert('0')
        self.clear_flag = True

    def equ(self, num):
        self.num_pad.setEnabled(0)
        if self.equGetDisplay_flag is True:
            self.num = int(num.replace(',', ''))
        sum = self.read()

        if self.operator == "mns":
            sum = sum - self.num
        elif self.operator == "pls":
            sum = sum + self.num

        self.clear_flag = True
        self.write(sum)
        self.displayInsert(sum)
        self.equGetDisplay_flag = False
        self.num_pad.setEnabled(1)

    def displayInsert(self, data):
        if type(data) is not int:
            data = int(data.replace(',', ''))
        self.display.clear()
        self.display.insert('{:,}'.format(data))

    def insert_num(self, num):
        if self.clear_flag:
            self.display.clear()
            self.clear_flag = False
        data = self.display.text() + num
        if len(data) < 17:
            self.displayInsert(data)

    def read(self):
        uid, data = rfid.read()

        if data == "Authentication error":
            self.display.clear()
            self.display.insert(data)
            return -1

        self.displayInsert(data)
        self.clear_flag = True
        return data

    def write(self, data):
        try:
            rfid.write(data)
        except ValueError:
            self.display.clear()
            self.display.insert("Error")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()
    # frame.showFullScreen()
    frame.show()
    app.exec_()
