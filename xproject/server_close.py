import socket
import argparse
port = 65000

def opendoor():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 지정한 host와 prot를 통해 서버에 접속합니다.
    client_socket.connect(("192.168.0.215", port))
    sendData = "open"
    client_socket.sendall(sendData.encode('utf-8'))

    # 소켓을 닫는다.
    client_socket.close()
