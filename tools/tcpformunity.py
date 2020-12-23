# -*-coding:GBK-*-
import socket

global tcpSockets
global tcpLogSockets
global severIP


def log_from_unity_tcp(severIP):
    with open("./log/unity_log.txt", "a") as unity_log:
        unity_log.write("系统时间\t运行时间\t障碍物距离\t当前速度" + "\n"
                        + "系统时间\t运行时间\t轮椅位置\t操作\n")
    unity_log.close()

    tcpLogSockets = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpLogSockets.bind(("127.0.0.1", 8084))
    tcpLogSockets.connect(severIP)

    while True:
        _recv_data = tcpLogSockets.recv(2048)
        if len(_recv_data) != 0:
            recv_data = _recv_data.decode("UTF-8")
            print("from unity = {}".format(recv_data))
            with open("./log/unity_log.txt", "a") as unity_log:
                unity_log.write(recv_data + "\n")
            unity_log.close()
