#!/usr/local/bin/python3

import sys
import serial
import binascii
from time import sleep

def main():
    args = sys.argv
    ser = serial.Serial('/dev/tty.usbserial-A506MR12', parity=serial.PARITY_NONE)

    ser.baudrate = 115200
    device_id = 0x01

    # AUTO/MANUALセット（MANUAL)
    send = get_bytes(device_id, 0x70, '01')
    print("-->\t" + core(send))
    ser.write(send)
    print("<--\t" + core(ser.readline()))

    # アラーム確認
    send = get_bytes(device_id, 0x5b)
    print("-->\t" + core(send))
    ser.write(send)
    print("<--\t" + core(ser.readline()))
    ser.close()

def core(line):
    linebytes = binascii.hexlify(line)
    response = linebytes[2:len(linebytes)-8]
    device_id = response[0:2]
    cmd_no = response[2:4]
    data = response[4:len(response)]
    ret = "ID: " + str(device_id, "utf-8") + "\tCMD: " + str(cmd_no, "utf-8") + "\tDATA: " + str(data, "utf-8")
    return ret

def get_crc(cmd_no, data=None):
    crc_data = cmd_no
    if data is not None:
        crc_data += binascii.unhexlify(data)
    ret_int = binascii.crc_hqx(crc_data,0)
    ret = ret_int.to_bytes(2,'big')
    return ret

def get_bytes(device_id, cmd_no, data=None):
    device_id = device_id.to_bytes(1, 'big')
    cmd_no = cmd_no.to_bytes(1, 'big')
    crc = get_crc(cmd_no, data)
    ret = b'\xef' + device_id + cmd_no
    if data is not None:
        ret += binascii.unhexlify(data)
    return  ret + crc + b'\x0d\x0a'

if __name__ == '__main__':
    main()

