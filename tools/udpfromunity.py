import socket
from time import sleep


def speed_form_unity():
    """
    接收从unity传入的速度数据，此函数会监听本机网络端口8081，每调用一次会返回一次receive_data，udp网络传输的特点：你随便发，我想接就接，
    unity发送速度占用8080端口，此函数接收速度占用8081端口。

    Parameters
    ----------
    :return: 从8081端口接收到的速度数据
    """
    # 使用udp接收数据 IPV4 udp

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 绑定端口号
    s.bind(("127.0.0.1", 8081))

    # 接受数据并打印输出
    receive_data = s.recvfrom(1024)  # 函数recvfrom()内参数表示接受的数据最大值，接受到的数据是元组
    receive_data = float(receive_data[0].decode())
    print("1--unity_speed = {}".format(receive_data))  # 数据解码decode()

    # 关闭socket
    s.close()

    return receive_data


def control_code_to_unity_udp(control_code):

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("127.0.0.1", 8085))
    s.sendto(bytes(control_code, "ascii"), ("127.0.0.1", 8082))
    s.close()


def log_from_unity():
    """
    接收从unity中8083端口传回的日志数据，此函数占用8084端口接收。

    :return: 接收到的字符串数据
    """

    with open("./log/unity_log.txt", "a") as unity_log:
        unity_log.write("系统时间\t运行时间\t障碍物距离\t当前速度" + "\n")
    unity_log.close()

    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(("127.0.0.1", 8084))
        receive_data = s.recvfrom(1024)
        receive_data = receive_data[0].decode()
        print("3--unity_log:{}".format(receive_data))
        with open("./log/unity_log.txt", "a") as unity_log:
            unity_log.write(receive_data + "\n")
        unity_log.close()
        s.close()
        sleep(0.1)
