import socket


def speed_form_unity():
    """
    接收从unity传入的数据，此函数会监听本机网络端口8081，每调用一次会返回一次receive_data，udp网络传输的特点：你随便发，我想接就接。

    Parameters
    ----------
    :return: 从8081端口接收到的数据
    """
    # 使用udp接收数据 IPV4 udp

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 绑定端口号
    s.bind(("127.0.0.1", 8081))

    # 接受数据并打印输出
    receive_data = s.recvfrom(1024)  # recvfrom内参数表示接受的数据最大值，接受到的数据是元组
    receive_data = float(receive_data[0].decode())
    print("1--unity_speed = {}".format(receive_data))  # 数据解码decode()

    # 关闭socket
    s.close()

    return receive_data
