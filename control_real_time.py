import socket
import cv2
import struct
import time
import serial #module for serial port communication
import signal
import sys
import numpy as np
import cv2
# from picamera import PiCamera, Color
# from sshkeyboard import listen_keyboard, stop_listening

cnt = 0
flag = 0
duration = 0
import time
from time import sleep
# demoCamera = PiCamera()
# demoCamera.rotation = 180
# demoCamera.resolution = (1920,1080)
# demoCamera.framerate = 24
ser = serial.Serial('/dev/serial0', 9600, timeout=1)
ser.write("h".encode('utf-8'))
response = ser.readline().decode('utf-8')
if response == "Hi Pi":
    print("Pi is ready")
    

def send_image(conn, img):
    img_encoded = cv2.imencode('.jpg', img)[1]
    data = img_encoded.tobytes()
    retries = 5
    conn.sendall(struct.pack("<L", len(data)))
    conn.sendall(data)
    
def press(key):
    user = key + '\n'
    ser.write(user.encode('utf-8'))

def main():
    server_address = ('192.168.137.142', 5001)
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sender_socket.connect(server_address)
    cap = cv2.VideoCapture(0)  # 使用摄像头(通常为0)
    if not cap.isOpened():
        print("Error: Unable to open camera")
        return

    try:
        while True:
            ret, frame = cap.read()
            
            if not ret:
                print("Error: Unable to capture frame")
                break
            if frame is not None:
                send_image(sender_socket, frame)
                time.sleep(0.1)  # 每隔1秒发送一次
                # 接收运动命令
                motion_command = sender_socket.recv(1024).decode()
                print("Received motion command:", motion_command)
                press(motion_command)
                time.sleep(0.1)
    finally:
        cap.release()
        sender_socket.close()

if __name__ == '__main__':
    main()