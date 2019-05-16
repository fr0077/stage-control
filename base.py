#!/usr/local/bin/python3

import serial
import binascii
from time import sleep

TIMEOUT=5
DIRECTION = {'PLUS':'01', 'MINUS':'02'}
AXIS = {'X':0x00, 'Y':0x01, 'Z':0x02}
SER = {0x00:ser_x, 0x01:ser_y, 0x01:ser_z}
SPEED = {'01':38400, '02':57600, '03':115200}

ser_x = serial.Serial('/dev/tty.usbserial-A506MR12', parity=serial.PARITY_NONE, timeout=TIMEOUT)
ser_x.baudrate = SPEED['03']
ser_y = serial.Serial('/dev/tty.usbserial-A506MR12', parity=serial.PARITY_NONE, timeout=TIMEOUT)
ser_y.baudrate = SPEED['03']
ser_z = serial.Serial('/dev/tty.usbserial-A506MR12', parity=serial.PARITY_NONE, timeout=TIMEOUT)
ser_z.baudrate = SPEED['03']

def set_communication_speed(device_id, speed):
    send = get_bytes(device_id, 0x02, speed)
    SER[device_id].write(send)
    printResult(SER[device_id].readline())

def get_servo_status(device_id):
    send = get_bytes(device_id, 0x15)
    SER[device_id].write(send)
    printResult(SER[device_id].readline())

def get_zero_status(device_id):
    send = get_bytes(device_id, 0x16)
    SER[device_id].write(send)
    printResult(SER[device_id].readline())

def set_manual(device_id):
    # AUTO/MANUALセット（MANUAL)
    send = get_bytes(device_id, 0x70, '01')
    SER[device_id].write(send)
    printResult(SER[device_id].readline())

def printResult(result):
    if result:
        print(core(result))
    else:
        print("TIMEOUT")

def get_current_position(device_id):
    send = get_bytes(device_id, 0x17)
    SER[device_id].write(send)
    printResult(SER[device_id].readline())

def check_alm(device_id):
    # アラーム確認
    send = get_bytes(device_id, 0x5b)
    SER[device_id].write(send)
    printResult(SER[device_id].readline())

def reset_alm(device_id):
    # アラームリセット
    send = get_bytes(device_id, 0x5c)
    SER[device_id].write(send)
    printResult(SER[device_id].readline())

def get_current(device_id):
    # 電流指令値取得
    send = get_bytes(device_id, 0x34)
    SER[device_id].write(send)
    printResult(SER[device_id].readline())

def servo_on(device_id):
    # サーボON
    send = get_bytes(device_id, 0x0b)
    SER[device_id].write(send)
    printResult(SER[device_id].readline())

def write_speed(device_id, speed):
    # パラメーター書き込み
    # パラメーターNo.16（速度）[mm/s]
    bytes_speed = speed.to_bytes(4, 'little').hex()
    send = get_bytes(device_id, 0x25, '1000' + bytes_speed)
    SER[device_id].write(send)
    printResult(SER[device_id].readline())

def write_distance(device_id, dist):
    # パラメーター書き込み
    # パラメーターNo.31（距離）[0.1um]
    bytes_dist = dist.to_bytes(4, 'little').hex()
    send = get_bytes(device_id, 0x25, '1f00' + bytes_dist)
    SER[device_id].write(send)
    printResult(SER[device_id].readline())
    
def set_offset(device_id, offset):
    # パラメーター書き込み
    # パラメーターNo.6（距離）[0.1um]
    bytes_offset = offset.to_bytes(4, 'little').hex()
    send = get_bytes(device_id, 0x25, '0600' + bytes_offset)
    SER[device_id].write(send)
    printResult(SER[device_id].readline())

def zero(device_id):
    send = get_bytes(device_id, 0x0d, '01')
    SER[device_id].write(send)
    printResult(SER[device_id].readline())

def move(device_id, direction):
    # パラメーター書き込みで指定した速度・位置で移動
    # インチング（正方向）
    send = get_bytes(device_id, 0x11, direction)
    SER[device_id].write(send)
    printResult(SER[device_id].readline())

def core(line):
    linebytes = binascii.hexlify(line)
    response = linebytes[2:len(linebytes)-8]
    device_id = response[0:2]
    cmd_no = response[2:4]
    data = response[4:len(response)]
    ret = str(data, "utf-8")
    ret_array = [ret[i: i+2] for i in range(0, len(ret), 2)]
    return ' '.join(ret_array)

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

