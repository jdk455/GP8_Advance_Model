import socket
import cv2
import struct
import time
import serial #module for serial port communication
import signal
import threading
import sys
import numpy as np
import cv2
# from picamera import PiCamera, Color
# from sshkeyboard import listen_keyboard, stop_listening

cnt = 0
flag = 0
duration = 0
status_code = "None"
import time
from time import sleep
# demoCamera = PiCamera()
# demoCamera.rotation = 180
# demoCamera.resolution = (1920,1080)
# demoCamera.framerate = 24
ser = serial.Serial('/dev/serial0', 9600, timeout=1)
# ser3 = serial.Serial('/dev/serial3', 9600, timeout=1)
# ser.write("h".encode('utf-8'))
# response = ser.readline().decode('utf-8')
# if response == "Hi Pi":
#     print("Pi is ready")



def listen_to_ser3():
    global status_code
    while True:
        if ser.in_waiting > 0:
            status_code = ser.read().decode('utf-8')
            print("Received from ser3: ", status_code)
    

def send_image(conn, img):
    global status_code
    img_encoded = cv2.imencode('.jpg', img)[1]
    data = img_encoded.tobytes()
    retries = 5
    conn.sendall(struct.pack("<L", len(data)))
    conn.sendall(data)
    conn.sendall(status_code.encode())
    
def press(key):
    user = key + '\n'
    ser.write(user.encode('utf-8'))

def main():
    # 创建并开始新线程
    t = threading.Thread(target=listen_to_ser3)
    t.start()
    server_address = ('192.168.137.199', 5001)
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sender_socket.connect(server_address)
    cap = cv2.VideoCapture(0)  # 使用摄像头(通常为0)
    if not cap.isOpened():
        print("Error: Unable to open camera")
        return

    try:
        while True:
            print("准备读取摄像头")
            ret, frame = cap.read()
            print("已经读取摄像头")
            if not ret:
                print("Error: Unable to capture frame")
                break
            if frame is not None:
                print("准备发送图片和返回码")
                send_image(sender_socket, frame)
                print("已经发送图片和返回码")
                time.sleep(0.1)  # 每隔1秒发送一次
                # 接收运动命令
                motion_command = sender_socket.recv(1024).decode()
                print("Received motion command:", motion_command)
                press(motion_command)
                print("Sent motion command:", motion_command)
          
    finally:
        cap.release()
        sender_socket.close()

if __name__ == '__main__':
    main()