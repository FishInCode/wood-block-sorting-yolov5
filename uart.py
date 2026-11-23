import serial as ser
import struct
import time

se = ser.Serial("/dev/ttyUSB0", 115200, timeout=10)

def Serial_Send(address, state):
    frame_header = b'\xFF'         
    frame_end = b'\xFE'
    data = struct.pack(
    '>BBBB', 
    frame_header[0], 
    address, 
    state, 
    frame_end[0]
    )
    se.write(data)
    se.flush()

def Serial_Receive():
    data = se.read_all()
    return data

