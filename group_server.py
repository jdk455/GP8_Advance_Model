import cv2
import cv2.aruco as aruco
import numpy as np
import sys
import socket
import cv2
import numpy as np
import struct
import pickle
from scipy.spatial.transform import Rotation as R
from typing import Tuple



row_num = 6
col_num = 7
# Define the size of the ArUco markers in meters
marker_size = 0.05
square_size = 0.01  # 7.5 cm

# Termination criteria for refining chessboard corners
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Define ArUco dictionary
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

def Control_Car(p1, p2, p3, p4, cx, cy, yaw, FRAME_WIDTH, FRAME_HEIGHT, CENTER_X, CENTER_Y, YAW_THRESHOLD)->Tuple[str,str,bool]: 
    # 计算ArUco码的宽度和高度
    # print("p1:",p1)
    # print("p2:",p2)
    # print("p3:",p3)
    # print("p4:",p4)
    aruco_width = np.linalg.norm(p1 - p2)
    aruco_height = np.linalg.norm(p1 - p4)
    # print("aruco_width:",aruco_width)
    # print("aruco_height:",aruco_height) 

    # 计算ArUco码在视野中所占的比例
    aruco_area = aruco_width * aruco_height
    frame_area = FRAME_WIDTH * FRAME_HEIGHT
    aruco_ratio = aruco_area / frame_area
    print("aruco_ratio",aruco_ratio)
    should_stop=False
    
    # 定义运动指令
    motion_command = "m"
    bias="a"
    
    if aruco_ratio<0.05:
        if cx < CENTER_X-15:        
            motion_command = "d"  #"左转"
            bias="a"
        elif cx > CENTER_X+15:            
            motion_command ="a" #"右转"
            bias="d"
        else:
            motion_command ="w" #"前进"
    else:
        should_stop=True
        motion_command = "m"#"停车"
    print("运动指令",motion_command)
    return motion_command,bias,should_stop





class MarkerServer:
    def __init__(self,conn) -> None:
        self.conn=conn
        self.state="global_info"
        self.calibrate_samples_num=10
        self.calibrate_count=0
        # Prepare object points
        self.objp = np.zeros((row_num*col_num,3), np.float32)
        self.objp[:,:2] = np.mgrid[0:col_num,0:row_num].T.reshape(-1,2)*square_size
        # Arrays to store object points and image points from all the images
        self.objpoints = [] # 3d point in real world space
        self.imgpoints = [] # 2d points in image plane
        self.is_load_calibration_result=True
        self.last_state=None
        self.bias="left"
        self.marker_list=list(range(50))
    
    def global_info_func(self)->None:
        if self.last_state!="global_info":
            print("进入全局信息状态")
            self.last_state="global_info"
        self.FRAME_HEIGHT, self.FRAME_WIDTH = self.frame.shape[:2]
        self.CENTER_X, self.CENTER_Y = self.FRAME_WIDTH // 2, self.FRAME_HEIGHT // 2 
        self.YAW_THRESHOLD = 10  # Adjust this value based on your specific situation
        print("FRAME_HEIGHT",self.FRAME_HEIGHT)
        print("FRAME_WIDTH",self.FRAME_WIDTH)
        print("CENTER_X",self.CENTER_X)
        print("CENTER_Y",self.CENTER_Y)
        
    
    def calibrate_func(self)->bool:
        if self.last_state!="calibrate":
            print("进入标定状态")
            self.last_state="calibrate"
        if self.is_load_calibration_result:
            self.calibration_result = pickle.load(open("calibration_result.p", "rb"))
            print("Camera calibration result loaded from 'calibration_result.p'")
            return True
        if self.calibrate_count<self.calibrate_samples_num:
            self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            # Find the chess board corners
            ret, corners = cv2.findChessboardCorners(self.gray, (7,6), None)
            # If found, add object points, image points (after refining them)
            if ret == True:
                self.calibrate_count+= 1
                self.objpoints.append(self.objp)
                corners2 = cv2.cornerSubPix(self.gray, corners, (11, 11), (-1, -1), criteria)
                self.imgpoints.append(corners2)
                print(f"Sample {self.calibrate_count} collected")
            return False
        else:
            # Perform calibration
            ret, cameraMatrix, distCoeffs, rvecs, tvecs = cv2.calibrateCamera(self.objpoints, self.imgpoints, self.gray.shape[::-1], None, None)
            # Save the camera calibration result for later use
            self.calibration_result = {"cameraMatrix": cameraMatrix, "distCoeffs": distCoeffs}
            pickle.dump(self.calibration_result, open("calibration_result.p", "wb"))
            print("Camera calibration completed and saved to 'calibration_result.p'")
            return True
        
    def detect_func(self)->Tuple[bool, int]:
        if self.last_state!="detect":
            print("进入检测状态")
            self.last_state="detect"
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY) 
        corners, ids, _ = aruco.detectMarkers(gray, aruco_dict)
        if ids==None:
            return False,-1
        all_ids=[i[0] for i in ids]
        for i in all_ids:
            if i in self.marker_list:
                return True,i
        return False,-1
        
    
    def heading_func(self,heading_id)->Tuple[int, str]:
        motion_command="m"
        if self.last_state!="heading":
            print("进入前进状态，寻找目标",heading_id)
            self.last_state="heading"
            # Initialize lists to store values
            # self.yaw_list = []
            # self.pitch_list = []
            # self.roll_list = []
            # self.corner_points_list = []  # Each element will be a list of 4 corner points
            # self.center_points_list = []  # Each element will be a center point (cx, cy)
            # self.motion_command_list = []  # Each element will be a motion command
                
        # Detect ArUco markers
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY) 
        corners, ids, _ = aruco.detectMarkers(gray, aruco_dict)
        # cameraMatrix = self.calibration_result["cameraMatrix"]
        # distCoeffs = self.calibration_result["distCoeffs"]
        # If markers are detected
        if ids==None:

            return 0,motion_command #没有找到目标
        all_ids=[i[0] for i in ids]
        if heading_id not in all_ids:
            return 0,motion_command #没有找到目标
        else:
            i=all_ids.index(heading_id)
            # Draw polygon around the marker 
            self.frame = cv2.polylines(self.frame, [np.int32(corners[i])], True, (0,255,0), 3)
            # Get the coordinates of all the corner points of the marker
            for j in range(len(corners[i][0])):
                x, y = corners[i][0][j]
                # Draw corner point and display its coordinates
                self.frame = cv2.circle(self.frame, (int(x), int(y)), 5, (0,0,255), -1)
                self.frame = cv2.putText(self.frame, f"P{j+1}({x:.1f}, {y:.1f})", (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2)
            # Get the center of the marker and the orientation
            cx, cy = np.mean(corners[i][0], axis=0)
            center = (int(cx), int(cy))
            # print all the corners
            print(f"Marker {ids[i][0]}: C({cx:.1f}, {cy:.1f}) P1({corners[i][0][0][0]:.1f}, {corners[i][0][0][1]:.1f}), P2({corners[i][0][1][0]:.1f}, {corners[i][0][1][1]:.1f}), P3({corners[i][0][2][0]:.1f}, {corners[i][0][2][1]:.1f}), P4({corners[i][0][3][0]:.1f}, {corners[i][0][3][1]:.1f})  ")
            self.frame = cv2.circle(self.frame, center, 5, (0,0,255), -1)
            self.frame = cv2.putText(self.frame, f"C({cx:.1f}, {cy:.1f})", center, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2)
            motion_command,self.bias,should_stop=Control_Car(corners[i][0][0], corners[i][0][1], corners[i][0][2], corners[i][0][3], cx, cy, None, self.FRAME_WIDTH, self.FRAME_HEIGHT, self.CENTER_X, self.CENTER_Y, self.YAW_THRESHOLD)
            if should_stop:
                return 2,motion_command
            else:
                return 1,motion_command
            # # Estimate pose
            # rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners[i], marker_size, cameraMatrix, distCoeffs)

            # # Convert rotation vector to rotation matrix
            # rmat, _ = cv2.Rodrigues(rvec[0])

            # # Convert rotation matrix to Euler angles
            # rotation = R.from_matrix(rmat)
            # euler_angles = rotation.as_euler('zyx', degrees=True)

            # yaw  = euler_angles[1]
            # pitch= euler_angles[0]
            # roll = euler_angles[2]
            
            # # Add the new values to the respective lists
            # self.yaw_list.append(yaw)
            # self.pitch_list.append(pitch)
            # self.roll_list.append(roll)
            # assert len(self.yaw_list) == len(self.pitch_list) == len(self.roll_list)
            # if len(self.yaw_list) > 10:
            #     # Remove outliers
            #     yaw_list = remove_outliers(self.yaw_list)
            #     pitch_list = remove_outliers(self.pitch_list)
            #     roll_list = remove_outliers(self.roll_list)
            #     # Calculate the averages
            #     yaw_avg = np.mean(yaw_list)
            #     pitch_avg = np.mean(pitch_list)
            #     roll_avg = np.mean(roll_list)
            #     # Remove the oldest values
            #     self.yaw_list.pop(0)
            #     self.pitch_list.pop(0)
            #     self.roll_list.pop(0)
            #     print(f"Yaw: {yaw_avg}, Pitch: {pitch_avg}, Roll: {roll_avg}"
            
            # 发送运动命令到客户端
            # self.motion_command_list.append(motion_command)
            # if len(motion_command)>10:
            #     #获取最多的指令
            #     motion_command = max(self.motion_command_list, key=self.motion_command_list.count)
            # motion_command_list=[]
            
        
    def loss_func(self,heading_id)->Tuple[bool,str]:
        if self.last_state!="loss":
            print("丢失目标",heading_id,"正在调整")
            self.last_state="loss"
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY) 
        corners, ids, _ = aruco.detectMarkers(gray, aruco_dict)
        if ids==None:
            return False,self.bias
        
        # If markers are detected
        all_ids=[i[0] for i in ids]
        if heading_id in all_ids:
            return True,"m"
        return False,self.bias
                
        
                
        
        
    def forward_a_frame(self,frame):
        motion_command="m"
        self.frame=frame
        if self.state=="global_info":
            self.global_info_func()
            self.state="calibrate"
        elif self.state=="calibrate":
            if self.calibrate_func():
                self.state="detect"
        elif self.state=="detect":
            motion_command="a"
            if len(self.marker_list)!=0:
                result, self.heading_id=self.detect_func()
                if result:
                    self.state="heading"
                    self.marker_list.remove(self.heading_id)
            else:
                print("所有目标已经投喂完毕")
                sys.exit(0)
                
        elif self.state=="heading":
            result,motion_command=self.heading_func(self.heading_id)
            if result==0:
                self.state="loss"
            elif result==2:
                self.state="feed"
        
        elif self.state=="feed":
             print("投喂目标",self.heading_id)
             self.state="detect"
        
        elif self.state=="loss":
            result,motion_command=self.loss_func(self.heading_id)
            if result:
                self.state="heading"
            
            
        cv2.imshow('frame', self.frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            sys.exit(0)
        self.conn.sendall(motion_command.encode())

def remove_outliers(data, axis=None):
    q25, q75 = np.percentile(data, [25, 75], axis=axis)
    iqr = q75 - q25
    lower_bound = q25 - 1.5 * iqr
    upper_bound = q75 + 1.5 * iqr
    return [d for d in data if lower_bound <= d <= upper_bound]

def recvall(sock, count):
    buf = b''
    while count > 0:
        newbuf = sock.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf

# 设置服务器地址和端口
#192.168.137.166
server_address = ('0.0.0.0', 5001)

# 创建socket对象
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)


# 开始监听
server_socket.listen(1)

print("等待连接...")
conn, addr = server_socket.accept()
print(f"连接到：{addr}")

marker_server=MarkerServer(conn)

# try:
while True:
    # 接收图像数据长度
    length = struct.unpack('<L', recvall(conn, 4))[0]

    # 接收图像数据
    frame_data = recvall(conn, length)

    # 将字节串转换为numpy数组并解码
    frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)
    # frame_reverse= cv2.flip(frame, 0).astype(np.uint8)
    # 显示图像
    marker_server.forward_a_frame(frame)
    # print("frame.shape",frame.shape)
    # cv2.imshow('frame', frame)
    # cv2.waitKey(10)
    
    




