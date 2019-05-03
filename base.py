#!/usr/local/bin/python3

import serial
import binascii
from time import sleep

ser = serial.Serial('/dev/tty.usbserial-A506MR12', parity=serial.PARITY_NONE, timeout=10)
ser.baudrate = 115200
DIRECTION = {'PLUS':'01', 'MINUS':'02'}
AXIS = {'X':0x00, 'Y':0x01, 'Z':0x02}

def set_manual(device_id):
    # AUTO/MANUALセット（MANUAL)
    send = get_bytes(device_id, 0x70, '01')
    ser.write(send)
    printResult(ser.readline())

def printResult(result):
    if result:
        print(core(result))
    else:
        print("TIMEOUT")

def get_current_position(device_id):
    send = get_bytes(device_id, 0x17)
    ser.write(send)
    printResult(ser.readline())

def check_alm(device_id):
    # アラーム確認
    send = get_bytes(device_id, 0x5b)
    ser.write(send)
    printResult(ser.readline())

def reset_alm(device_id):
    # アラームリセット
    send = get_bytes(device_id, 0x5c)
    ser.write(send)
    printResult(ser.readline())

def get_current(device_id):
    # 電流指令値取得
    send = get_bytes(device_id, 0x34)
    ser.write(send)
    printResult(ser.readline())

def servo_on(device_id):
    # サーボON
    send = get_bytes(device_id, 0x0b)
    ser.write(send)
    printResult(ser.readline())

def write_speed(device_id, speed):
    # パラメーター書き込み
    # パラメーターNo.16（速度）[mm/s]
    bytes_speed = speed.to_bytes(4, 'little').hex()
    send = get_bytes(device_id, 0x25, '1000' + bytes_speed)
    ser.write(send)
    printResult(ser.readline())

def write_distance(device_id, dist):
    # パラメーター書き込み
    # パラメーターNo.31（距離）[0.1um]
    bytes_dist = dist.to_bytes(4, 'little').hex()
    send = get_bytes(device_id, 0x25, '1f00' + bytes_dist)
    ser.write(send)
    printResult(ser.readline())

def zero(device_id):
    #  原点復帰（各機器に設定された値）
    send = get_bytes(device_id, 0x0d, '01')
    ser.write(send)
    printResult(ser.readline())

def move(device_id, direction):
    # パラメーター書き込みで指定した速度・位置で移動
    # インチング（正方向）
    send = get_bytes(device_id, 0x11, direction)
    ser.write(send)
    printResult(ser.readline())

def core(line):
    linebytes = binascii.hexlify(line)
    response = linebytes[2:len(linebytes)-8]
    device_id = response[0:2]
    cmd_no = response[2:4]
    data = response[4:len(response)]
    ret = str(data, "utf-8")
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

