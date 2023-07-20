import socket
import cv2
import struct
import time

def send_image(conn, img):
    img_encoded = cv2.imencode('.jpg', img)[1]
    data = img_encoded.tobytes()
    retries = 5
    conn.sendall(struct.pack("<L", len(data)))
    conn.sendall(data)

def main():
    server_address = ('localhost', 5001)
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
                time.sleep(0.1)
                
    finally:
        cap.release()
        sender_socket.close()

if __name__ == '__main__':
    main()