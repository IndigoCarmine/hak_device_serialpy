from abc import ABC, ABCMeta, abstractmethod
import asyncio
from concurrent.futures import ThreadPoolExecutor
import enum
import threading
import serial
import time
from cobs import cobs

def cobs_encode(data: bytes):
    try:
        return cobs.encode(data) + b"\x00"
    except:
        return b""


def cobs_decode(data: bytes):
    try:
        return cobs.decode(data[:-1])
    except:
        return b""

class HAKDevice(ABC):
    def __init__(self, port):
        self.ser = serial.Serial(port=port)

  
    def write(self, data: bytes):
        encode = cobs_encode(data)
        self.ser.write(encode)

    def read(self):
        u = self.ser.read_until(b'\x00')
        decode = cobs_decode(u)
        return decode

    def read_raw(self):
        u = self.ser.read_all()
        if u != b'':
            print(u)

class HAKServoDevice(HAKDevice):
    def __init__(self, port):
        super().__init__(port)

    def set_position(self, servo: int, position: int):
        self.write(bytes([servo, position]))

    def servo_activate(self, servo: int):
        self.write(bytes([0x2<<4,0x01<<servo]))
        self.write(bytes([0x2<<4,0x01<<servo]))
        self.write(bytes([0x2<<4,0x01<<servo]))
        self.write(bytes([0x2<<4,0x01<<servo]))



if __name__ == "__main__":
    device = HAKServoDevice("COM7")
    motorID = 0x02
    device.servo_activate(motorID)
    device.servo_activate(motorID)
    while True:

        device.set_position(motorID, 0x00)
        time.sleep(1)
        device.set_position(motorID, 0xFF)
        time.sleep(1)