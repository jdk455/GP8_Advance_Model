import threading
import re
# class CommandSender(threading.Thread):
#     def __init__(self, conn):
#         threading.Thread.__init__(self)
#         self.conn = conn

#     def run(self):
#         while True:
while(True):
    # 获取用户输入的字段
    fields = input("请输入方向模式(F(前进),B(后退),L(逆时针),R(顺时针),l(左转),r(右转)：")
    motor_command = ""
    try:
        # 判断第一个字段是否是F或B
        if fields[0] in ['F', 'B']:
            # 第二个字段设置电机速度
            speed =  int(input("请设置电机速度(0-255)："))
            #speed要在0-255之间
            if speed > 255:
                speed = 255
            elif speed < 0:
                speed = 0
            # 打印结果
            print(f'M0{fields[0]}{speed}')
            motor_command = f'M0{fields[0]}{speed}'

        # 判断第一个字段是否是L、l、R或r
        elif fields[0] in ['L', 'l', 'R', 'r']:
            # 第二个字段设置电机编号，只能接收0-3的数字
            motor_number = int(input("请设置电机编号(0-3)："))
            #motor_number要在0-3之间
            if motor_number > 3:
                motor_number = 3
            elif motor_number < 0:
                motor_number = 0
            # 第三个字段设置该编号电机的速度
            speed = int(input("请设置电机速度(0-255)："))
            #speed要在0-255之间
            if speed > 255:
                speed = 255
            elif speed < 0:
                speed = 0
            # 打印结果
            print(f'M{motor_number}{fields[0]}{speed}')
            motor_command = f'M{motor_number}{fields[0]}{speed}'

        else:
            print("输入的第一个字段无效。")
            continue
    except:
        print("发生错误，请检查输入。")
        continue
    print("电机命令")
    with open("motor_command/motor_command.txt", "w",encoding="utf-8") as f:
        f.write(motor_command)
