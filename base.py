#!/usr/local/bin/python3

import serial
import binascii
from time import sleep

ser = serial.Serial('/dev/tty.usbserial-A506MR12', parity=serial.PARITY_NONE)
ser.baudrate = 115200
POSITIVE = '01'
NEGATIVE = '02'

def main():
    set_manual()
    check_alm()
    reset_alm()
    servo_on()
    # zero()
    # sleep(10)
    write_speed(10)
    write_distance(800000)
    get_current()
    move(POSITIVE)

def set_manual():
    # AUTO/MANUALセット（MANUAL)
    print("SET MANUAL")
    send = get_bytes(device_id, 0x70, '01')
    print("-->\t" + core(send))
    ser.write(send)
    print("<--\t" + core(ser.readline()))

def check_alm():
    # アラーム確認
    print("CHECK ALM")
    send = get_bytes(device_id, 0x5b)
    print("-->\t" + core(send))
    ser.write(send)
    print("<--\t" + core(ser.readline()))

def reset_alm():
    # アラームリセット
    print("RESET ALM")
    send = get_bytes(device_id, 0x5c)
    print("-->\t" + core(send))
    ser.write(send)
    print("<--\t" + core(ser.readline()))

def get_current():
    # 電流指令値取得
    print("GET CURRENT")
    send = get_bytes(device_id, 0x34)
    print("-->\t" + core(send))
    ser.write(send)
    print("<--\t" + core(ser.readline()))

def servo_on():
    # サーボON
    print("SERVO ON")
    send = get_bytes(device_id, 0x0b)
    print("-->\t" + core(send))
    ser.write(send)
    print("<--\t" + core(ser.readline()))

def write_speed(speed):
    # パラメーター書き込み
    # パラメーターNo.16（速度）[mm/s]
    print("WRITE SPEED")
    bytes_speed = speed.to_bytes(4, 'little').hex()
    send = get_bytes(device_id, 0x25, '1000' + bytes_speed)
    print("-->\t" + core(send))
    ser.write(send)
    print("<--\t" + core(ser.readline()))

def write_acceleration(acceleration):
    # パラメーター書き込み
    # パラメーターNo.9（加減速度）[m/s^2]
    print("WRITE ACCELERATION")
    bytes_accel = acceleration.to_bytes(4, 'little').hex()
    send = get_bytes(device_id, 0x25, '0900' + bytes_accel)
    print("-->\t" + core(send))
    ser.write(send)
    print("<--\t" + core(ser.readline()))

def write_distance(dist):
    # パラメーター書き込み
    # パラメーターNo.31（距離）[0.1um]
    print("WRITE DISTANCE")
    bytes_dist = dist.to_bytes(4, 'little').hex()
    send = get_bytes(device_id, 0x25, '1f00' + bytes_dist)
    print("-->\t" + core(send))
    ser.write(send)
    print("<--\t" + core(ser.readline()))

def zero():
    #  原点復帰（各機器に設定された値）
    print("ZERO")
    send = get_bytes(device_id, 0x0d, '01')
    print("-->\t" + core(send))
    ser.write(send)
    print("<--\t" + core(ser.readline()))

def move(direction):
    # パラメーター書き込みで指定した速度・位置で移動
    # インチング（正方向）
    print("MOVE")
    send = get_bytes(device_id, 0x11, direction)
    print("-->\t" + core(send))
    ser.write(send)
    print("<--\t" + core(ser.readline()))

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

