#!/usr/bin/python

import sys, random, struct, time
from PySide.QtCore import *
from PySide.QtGui import *
from main_ui import Ui_MainWindow

import function
import pigpio

pi = pigpio.pi()

class transProcess(QThread):
    message = Signal(str)

    def __init__(self, num, parent=None):  
        super(transProcess,self).__init__(parent)  
        self.num = num
  
    def run(self):  
        rf = function.RFID()
        first_uid, first_sum = rf.read()
        first_sum = first_sum - self.num
        first_sum = struct.pack('8sq', '',first_sum)
        first_sum = [ord(first_sum[i]) for i in range(16)]
        rf = function.RFID()
        rf.write(first_sum)

        self.message.emit('Put another card')

        while True:
            rf = function.RFID()
            second_uid, second_sum = rf.read()
            self.msleep(100)
            if not second_uid == first_uid:
                second_sum = second_sum + self.num
                second_sum = struct.pack('8sq', '',second_sum)
                second_sum = [ord(second_sum[i]) for i in range(16)]
                rf = function.RFID()
                rf.write(second_sum)
                rf = function.RFID()
                second_uid, second_sum = rf.read()
                self.message.emit('{:,}'.format(second_sum))
                self.ring = Ring()
                return 0


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.operator = ''
        self.clear_flag = True

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
        self.bequ.clicked.connect(self.equ)
        self.bf2.clicked.connect(self.test)

        # self.setupUpdateThread()

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
    
    def test(self):
        self.ring = Ring()
        
    def mns(self):
        self.operator = "mns"
        self.clear_flag = True

    def pls(self):
        self.operator = "pls"
        self.clear_flag = True

    def cls(self):
        self.display.clear()
        self.display.insert('0')
        self.clear_flag = True

    def equ(self):
        num = int(self.display.text().replace(',',''))
        sum = self.read()

        if self.operator == "mns":
            sum = sum - num
        elif self.operator == "pls":
            sum = sum + num

        self.clear_flag = True
        self.write(sum)
        self.displayInsert(sum)

    def displayInsert(self, data):
        if type(data) is not int:
            data = int(data.replace(',',''))
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
        rf = function.RFID()
        uid, data = rf.read()

        if data == "Authentication error":
            self.display.clear()
            self.display.insert(data)
            return -1

        self.displayInsert(data)
        self.clear_flag = True
        self.ring = Ring()
        return data

    def write(self, input_data):
        rf = function.RFID()
        try:
            data = self.convertToHexList(input_data)
            rf.write(data)
        except ValueError:
            self.display.clear()
            self.display.insert("Error")

    def convertToHexList(self, str_data):
        hex_data = struct.pack('8sq', '',int(str(str_data).replace(',','')))
        hex_data = [ord(hex_data[i]) for i in range(16)]
        return hex_data


class Ring(QThread):
    def __init__(self,parent=None):  
        super(Ring,self).__init__(parent)  
        self.run()
  
    def run(self):  
        pi.write(12, 1)
        self.msleep(100)
        pi.write(12, 0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()
    # frame.showFullScreen()
    frame.show()
    app.exec_()
