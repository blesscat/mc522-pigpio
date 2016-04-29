#!/usr/bin/python

import sys, random, struct, time, threading, os
from PySide.QtCore import *
from PySide.QtGui import *
from main_ui import Ui_MainWindow

import function

class attr_frame():
    def __init__(self, bm5, bm1, lcd, bp1, bp5, num):
        self.bm5 = bm5
        self.bm1 = bm1
        self.lcd = lcd
        self.num = num
        self.bp1 = bp1
        self.bp5 = bp5

    def m5(self):
        self.num = self.lcd.intValue()
        self.num = self.num - 5
        self.check_num()

    def m1(self):
        self.num = self.lcd.intValue()
        self.num = self.num - 1
        self.check_num()

    def p1(self):
        self.num = self.lcd.intValue()
        self.num = self.num + 1
        self.check_num()

    def p5(self):
        self.num = self.lcd.intValue()
        self.num = self.num + 5
        self.check_num()

    def check_num(self):
        if self.num > 255:
            self.num = 255
        elif self.num < 0:
            self.num = 0
        self.lcd.display(self.num)
        web.send('attr:{0} {1} {2} {3} {4} {5}'.format(
                    attr1_lcd.intValue(),
                    attr2_lcd.intValue(),
                    attr3_lcd.intValue(),
                    attr4_lcd.intValue(),
                    attr5_lcd.intValue(),
                    attr6_lcd.intValue()))

class transProcess(QThread):
    message = Signal(str)
    result = Signal(int)
    

    def __init__(self, num, clear_flag, equGetDisplay_flag, operator,  parent=None):
        global gnum
        self.num = gnum = num
        self.clear_flag = clear_flag
        self.operator = operator
        if equGetDisplay_flag is False:
            self.num = gnum

        super(transProcess,self).__init__(parent)

    def run(self):
        uid, sum = rfid.read()

        if self.operator == "mns":
            sum = sum - self.num
            rfid.write(sum)
            self.clear_flag = True
            self.equGetDisplay_flag = False
            self.message.emit('{:,}'.format(sum))
            self.result.emit(0)

        elif self.operator == "pls":
            sum = sum + self.num
            rfid.write(sum)
            self.clear_flag = True
            self.equGetDisplay_flag = False
            self.message.emit('{:,}'.format(sum))
            self.result.emit(0)

        elif self.operator == "trans":
            first_uid, first_sum = rfid.read()
            first_sum = first_sum - self.num
            rfid.write(first_sum)

            self.message.emit('Put another card')

            while True:
                second_uid, second_sum = rfid.read()
                self.msleep(1000)
                if not second_uid == first_uid:
                    second_sum = second_sum + self.num
                    rfid.write(second_sum)
                    second_uid, second_sum = rfid.read()
                    self.message.emit('{:,}'.format(second_sum))
                    self.result.emit(0)
                    break
        else:
            self.result.emit(0)
        rfid.ring(2)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        
        global rfid, attr_rfid, web
        rfid = function.RFID(4)
        attr_rfid = function.RFID(5)
        web = function.sendto_web('127.0.0.1', 9999)
        # web = function.sendto_web('192.168.0.192', 21000)

        global attr1_lcd, attr2_lcd, attr3_lcd, attr4_lcd, attr5_lcd, attr6_lcd
        attr1_lcd = self.attr1_lcd
        attr2_lcd = self.attr2_lcd
        attr3_lcd = self.attr3_lcd
        attr4_lcd = self.attr4_lcd
        attr5_lcd = self.attr5_lcd
        attr6_lcd = self.attr6_lcd

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
        self.bf2.clicked.connect(self.test)
# ================================================================================= 

        attr1 = attr_frame(self.attr1_bm5, self.attr1_bm1,
                           self.attr1_lcd, self.attr1_bp1,
                           self.attr1_bp5, self.attr1_lcd.intValue())
        attr2 = attr_frame(self.attr2_bm5, self.attr2_bm1,
                           self.attr2_lcd, self.attr2_bp1,
                           self.attr2_bp5, self.attr2_lcd.intValue())
        attr3 = attr_frame(self.attr3_bm5, self.attr3_bm1,
                           self.attr3_lcd, self.attr3_bp1,
                           self.attr3_bp5, self.attr3_lcd.intValue())
        attr4 = attr_frame(self.attr4_bm5, self.attr4_bm1,
                           self.attr4_lcd, self.attr4_bp1,
                           self.attr4_bp5, self.attr4_lcd.intValue())
        attr5 = attr_frame(self.attr5_bm5, self.attr5_bm1,
                           self.attr5_lcd, self.attr5_bp1,
                           self.attr5_bp5, self.attr5_lcd.intValue())
        attr6 = attr_frame(self.attr6_bm5, self.attr6_bm1,
                           self.attr6_lcd, self.attr6_bp1,
                           self.attr6_bp5, self.attr6_lcd.intValue())

        self.attr1_bm5.clicked.connect(lambda: attr1.m5())
        self.attr1_bm1.clicked.connect(lambda: attr1.m1())
        self.attr1_bp1.clicked.connect(lambda: attr1.p1())
        self.attr1_bp5.clicked.connect(lambda: attr1.p5())
        self.attr2_bm5.clicked.connect(lambda: attr2.m5())
        self.attr2_bm1.clicked.connect(lambda: attr2.m1())
        self.attr2_bp1.clicked.connect(lambda: attr2.p1())
        self.attr2_bp5.clicked.connect(lambda: attr2.p5())
        self.attr3_bm5.clicked.connect(lambda: attr3.m5())
        self.attr3_bm1.clicked.connect(lambda: attr3.m1())
        self.attr3_bp1.clicked.connect(lambda: attr3.p1())
        self.attr3_bp5.clicked.connect(lambda: attr3.p5())
        self.attr4_bm5.clicked.connect(lambda: attr4.m5())
        self.attr4_bm1.clicked.connect(lambda: attr4.m1())
        self.attr4_bp1.clicked.connect(lambda: attr4.p1())
        self.attr4_bp5.clicked.connect(lambda: attr4.p5())
        self.attr5_bm5.clicked.connect(lambda: attr5.m5())
        self.attr5_bm1.clicked.connect(lambda: attr5.m1())
        self.attr5_bp1.clicked.connect(lambda: attr5.p1())
        self.attr5_bp5.clicked.connect(lambda: attr5.p5())
        self.attr6_bm5.clicked.connect(lambda: attr6.m5())
        self.attr6_bm1.clicked.connect(lambda: attr6.m1())
        self.attr6_bp1.clicked.connect(lambda: attr6.p1())
        self.attr6_bp5.clicked.connect(lambda: attr6.p5())

        self.attr_bzero.clicked.connect(self.attr_zero)
        self.attr_bread.clicked.connect(self.attr_read)
        self.attr_bwrite.clicked.connect(self.attr_write)

# ================================================================================= 
        self.bdice.clicked.connect(self.dice)
        self.brelease.clicked.connect(self.restart_self)

    def attr_zero(self):
        self.attr1_lcd.display(0)
        self.attr2_lcd.display(0)
        self.attr3_lcd.display(0)
        self.attr4_lcd.display(0)
        self.attr5_lcd.display(0)
        self.attr6_lcd.display(0)

    def attr_read(self):
        uid, data = attr_rfid.attr_read()
        self.attr1_lcd.display(data[0])
        self.attr2_lcd.display(data[1])
        self.attr3_lcd.display(data[2])
        self.attr4_lcd.display(data[3])
        self.attr5_lcd.display(data[4])
        self.attr6_lcd.display(data[5])
        attr_rfid.ring()
        web.send('attr:{0} {1} {2} {3} {4} {5}'.format(
                    data[0],
                    data[1],
                    data[2],
                    data[3],
                    data[4],
                    data[5]))

    def attr_write(self):
        data = [self.attr1_lcd.intValue(),
                self.attr2_lcd.intValue(),
                self.attr3_lcd.intValue(),
                self.attr4_lcd.intValue(),
                self.attr5_lcd.intValue(),
                self.attr6_lcd.intValue()]
        attr_rfid.attr_write(data)
        attr_rfid.ring(2)
        web.send('attr:{0} {1} {2} {3} {4} {5}'.format(
                    data[0],
                    data[1],
                    data[2],
                    data[3],
                    data[4],
                    data[5]))


    def test(self):
        self.display.clear()
        self.display.insert(str(threading.active_count()))

    def dice(self):
        dice = [self.dice1_label,
                self.dice2_label,
                self.dice3_label,
                self.dice4_label,
                self.dice5_label,
                self.dice6_label]
        self.dice_sum.setText('0')
        for i in range(len(dice)):
            dice[i].setText('0')
        for i in range(self.dice_spinbox.value()):
            dice_num = random.randint(1,6)
            try:
                sum = sum + dice_num
            except UnboundLocalError:
                sum = dice_num
            dice[i].setText(str(dice_num))
        self.dice_sum.setText(str(sum))
        web.send('dice:{0} {1} {2} {3} {4} {5}'.format(
                    self.dice1_label.text(),
                    self.dice2_label.text(),
                    self.dice3_label.text(),
                    self.dice4_label.text(),
                    self.dice5_label.text(),
                    self.dice6_label.text()))

    def updateText(self,text):
        self.display.clear()
        self.display.insert(text)
        web.send('lcd:' + text)
        self.clear_flag = True

    def enable_pad(self):
        self.num_pad.setEnabled(1)

    def equ(self, num):
        self.num_pad.setEnabled(0)
        if self.equGetDisplay_flag is True:
            self.num = int(num.replace(',' ,''))
        self.updateThread = transProcess(self.num,
                self.clear_flag, self.equGetDisplay_flag, self.operator)
        #connect our update functoin to the progress signal of the update thread
        self.updateThread.message.connect(self.updateText, Qt.QueuedConnection)
        self.updateThread.result.connect(self.enable_pad, Qt.QueuedConnection)
        if not self.updateThread.isRunning():#if the thread has not been started let's kick it off
            self.updateThread.start()
        self.clear_flag = True
        self.equGetDisplay_flag = False

    def trans(self):
        self.operator = "trans"
        self.clear_flag = True
        self.equGetDisplay_flag = True

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
        rfid.ring()
        web.send('lcd:{:,}'.format(data))
        return data

    def write(self, data):
        try:
            rfid.write(data)
            rfid.ring(2)
            web.send('lcd:' + data)
        except ValueError:
            self.display.clear()
            self.display.insert("Error")

    def restart_self(self):
        python = sys.executable
        os.execl(python, python, * sys.argv)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()
    # frame.showFullScreen()
    frame.show()
    app.exec_()
