# import RPi.GPIO as GPIO
import threading
import socket, struct, time

import pigpio
import MFRC522

class RFID():
    def __init__(self, sector):
        self.sector = sector
        self.pi = pigpio.pi()

    def read(self):
        rfid = RFID_function(self.sector)
        uid, data = rfid.read()
        # convert data to bytearray
        data = ''.join(chr(data[i]) for i in range(len(data)))
        # sturct={ char[8], long long},
        # assign the long long value with ',' to 'data'
        data = struct.unpack('8sq', data)[1]

        return uid, data

    def write(self, data):
        rfid = RFID_function(self.sector)
        if type(data) is str:
            data = int(data.replace(',' , ''))
        rfid.int_write(data)

    def attr_read(self):
        rfid = RFID_function(self.sector)
        uid,data = rfid.read()
        return uid, data

    def attr_write(self, data):
        rfid = RFID_function(self.sector)
        for i in range(16-len(data)):
            data.append(0)
        print(data)
        rfid.write(data)

    def ring(self, times=1):
        for i in range(times):
            self.pi.write(12, 1)
            time.sleep(0.1)
            self.pi.write(12, 0)
            time.sleep(0.05)


class RFID_function():
    def __init__(self, sector):
        self.MIFAREReader = MFRC522.MFRC522()
        self.sector = sector

    def read(self):
        while True:
            (status, TagType) = self.MIFAREReader.MFRC522_Request(
                                                self.MIFAREReader.PICC_REQIDL)

            # Get the UID of the card
            (status, uid) = self.MIFAREReader.MFRC522_Anticoll()

            if status == self.MIFAREReader.MI_OK:
                # string = str(uid[0]) + "," + str(uid[1]) + \
                #          "," + str(uid[2]) + "," + str(uid[3])

                # This is the default key for authentication
                key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
                # Select the scanned tag
                self.MIFAREReader.MFRC522_SelectTag(uid)

                # Authenticate
                status = self.MIFAREReader.MFRC522_Auth(
                         self.MIFAREReader.PICC_AUTHENT1A,
                         self.sector, key, uid)

                # Check if authenticated
                if status == self.MIFAREReader.MI_OK:
                    data = self.MIFAREReader.MFRC522_Read(self.sector)
                    self.MIFAREReader.MFRC522_StopCrypto1()
                else:
                    data = "Authentication error"

                return uid, data

    def write(self, data):
        while True:
            (status, TagType) = self.MIFAREReader.MFRC522_Request(
                                                self.MIFAREReader.PICC_REQIDL)

            # Get the UID of the card
            (status, uid) = self.MIFAREReader.MFRC522_Anticoll()

            if status == self.MIFAREReader.MI_OK:
                string = str(uid[0]) + "," + str(uid[1]) + \
                         "," + str(uid[2]) + "," + str(uid[3])

                # This is the default key for authentication
                key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
                # Select the scanned tag
                self.MIFAREReader.MFRC522_SelectTag(uid)

                # Authenticate
                status = self.MIFAREReader.MFRC522_Auth(
                         self.MIFAREReader.PICC_AUTHENT1A,
                         self.sector, key, uid)

                # Check if authenticated
                if status == self.MIFAREReader.MI_OK:
                    self.MIFAREReader.MFRC522_Write(self.sector, data)
                    self.MIFAREReader.MFRC522_StopCrypto1()
                else:
                    print("Authentication error")
                # GPIO.cleanup()
                return string

    def int_write(self, input_data):
        try:
            data = self.convertToHexList(input_data)
            self.write(data)
        except ValueError:
            data = "Error"
        return data

    def convertToHexList(self, str_data):
        hex_data = struct.pack('8sq', '', int(str(str_data).replace(',', '')))
        hex_data = [ord(hex_data[i]) for i in range(16)]
        return hex_data


class sendto_web():
    def __init__(self, udp_ip, udp_port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ip = udp_ip
        self.port = udp_port

    def send(self, message):
        self.sock.sendto(str(message), (self.ip, self.port))
        

class pass_message(threading.Thread):
    def __init__(self):
        super(pass_message, self).__init__()



