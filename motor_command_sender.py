import threading
import re
# class CommandSender(threading.Thread):
#     def __init__(self, conn):
#         threading.Thread.__init__(self)
#         self.conn = conn

#     def run(self):
#         while True:
while(True):
    motion_command = input("Enter command: ")
    if re.match(r'^M[1-4]S\d+$', motion_command):
        with open("motor_command.txt", "w",encoding="utf-8") as f:
            f.write(motion_command)
    else:
        print("Invalid command. Please enter a valid command, e.g. M1S255")