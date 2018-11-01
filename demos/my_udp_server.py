import socket

# SOCK_DGRAM指定了这个Socket的类型是UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 绑定端口
port = 9998
s.bind(('127.0.0.1', port))
print('Bind UDP on ' + str(port))

while True:
    # 接收数据:
    data, addr = s.recvfrom(1024)
    print(data, addr)
    print('Received from %s:%s.' % addr)
    s.sendto(b'Hello, %s!' % data, addr)
