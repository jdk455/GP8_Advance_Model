import socket
import json

# 创建 socket 对象
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



# 绑定端口
serversocket.bind(("0.0.0.0", 5002))

# 设置最大连接数，超过后排队
serversocket.listen(5)
direction=["F","B","L","R","l","r"]

while True:
    # 建立客户端连接
    clientsocket, addr = serversocket.accept()

    print("连接地址: %s" % str(addr))

    # 接收客户端消息
    data = clientsocket.recv(1024).decode('utf-8')
    values = [int(i) for i in json.loads(data)]
    print(values)
    print(len(values))
    for i,j in enumerate(values):
        print("M"+str(i%4)+direction[i//4]+"S"+str(j))
        
    print("从客户端接收的电机转速: ", values)

    clientsocket.close()