"""
虚拟现实环境情绪诱发平台-轮椅驱动程序-Python版本
程序接收从unity中传入的速度，将速度按照智能轮椅通讯协议转换后，数据输出到串口，驱动轮椅运行
2020-11-19 designed by 戚震
"""

from tools.wheelchair import *
from tools.udpfromunity import *
from tools.ctrlcodefromserial import *
from tools.tcpformunity import *
from time import sleep
import datetime
import threading

global recv_data
global tcpSockets
global sever_IP


def wheelchair_debug(port, run_times, wheelchair_speed):
    """
    轮椅直线运行测试函数，脚本运行时，轮椅以给定速度向前运行设定时间。
    2020-11-19 designed by qz。

    Parameters
    ----------
    :param port: RS232占用的端口号
    :param run_times: 测试时轮椅的运行时间
    :param wheelchair_speed: 测试时轮椅的运行速度
    :return: 无
    """
    wheelchair_serial = port_init(port)
    run_times = run_times * 10
    for i in range(run_times):
        print(datetime.datetime.now())
        if wheelchair_speed != 0:
            data = forward_straight_moving(wheelchair_speed)
            port_send_data(data, wheelchair_serial, wheelchair_speed)
        else:
            print("2---true_speed = 0.0")
        sleep(0.1)


def wheelchair_run_straight(port):
    """
    轮椅直线运行实验时使用此函数，输入RS232占用的端口号到此函数。
    此函数会自动接收从unity传入的速度，按通讯协议转换后输出到串口。
    2020-11-19 designed by qz。

    Parameters
    ----------
    :param port:RS232占用的端口号。
    :return:无。
    """
    wheelchair_serial = port_init(port)
    while True:
        print(datetime.datetime.now())
        wheelchair_speed = speed_form_unity()
        if wheelchair_speed != 0:
            data_send = forward_straight_moving(wheelchair_speed)
            port_send_data(data_send, wheelchair_serial, wheelchair_speed)
        else:
            print("2--true_speed = 0!!")
        sleep(0.1)


def recv_from_port(port, out="None"):
    """
    需要接收从轮椅串口传来的数据时使用，输入串口号，需要的数据类型，打印数据到控制台并保存到./log/recvdata_log.txt

    :param port: 串口号
    :param out: 数据类型，out2为控制杆数据
    :return: 无
    """

    wheelchair_serial = port_init(port)
    # recv_data_init(wheelchair_serial, out=out)

    while True:
        recv_data_init(wheelchair_serial, out=out)
        recv_data = wheelchair_serial.read_until()

        # print(datetime.datetime.now())

        print("recv_data = {}".format(recv_data))

        log_from_port(recv_data)
        sleep(0.09)


def send_control_code_to_unity_udp(port, out="out2"):
    """
    将串口接收的控制杆数据解析并通过udp传入unity，实现控制杆同时控制轮椅与unity中的轮椅。

    :param port: 串口号
    :param out: out2：控制杆数据
    :return: 无
    """

    wheelchair_serial = port_init(port)

    while True:
        recv_data_init(wheelchair_serial, out=out)
        recv_data = wheelchair_serial.read_until()

        # print(datetime.datetime.now())
        operator = control_code(recv_data)
        control_code_to_unity_udp(operator[0])
        print("operator = {}".format(operator[1]))
        print("recv_data = {}".format(recv_data))

        log_from_port(operator[1])  # 存操作码到./log/recvdata_log.txt
        sleep(0.09)


def send_control_code_to_unity_tcp(port, out="out2"):
    """
    轮椅控制杆操作信息串口传输到此脚本，然后tcp传输到unity控制虚拟轮椅运行。

    :param port: 串口端口号
    :param out: out2：控制杆数据
    :return: 无
    """

    # unity端tcp服务器地址
    severIP = ("127.0.0.1", 8083)
    # 控制码发送客户端，绑定8085端口
    tcpSockets = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpSockets.bind(("127.0.0.1", 8085))
    tcpSockets.connect(severIP)
    # 开启接收log线程，保存到./log/unity_log.txt
    recv_thread = threading.Thread(target=log_from_unity_tcp, args=(severIP,))
    recv_thread.start()
    # 开启串口
    wheelchair_serial = port_init(port)

    while True:
        # 每100ms向串口发送一个指令
        recv_data_init(wheelchair_serial, out=out)
        # 等待接收串口回传
        recv_data = wheelchair_serial.read_until()
        # 转换控制指令
        operator = control_code(recv_data)
        print("operator = {}".format(operator[1]))
        # 存储串口信息
        log_from_port(operator[1])  # 存操作码到./log/recvdata_log.txt
        # 发送控制指令到unity
        tcpSockets.sendto(bytes(operator[0], "ascii"), severIP)
        sleep(0.099)


if __name__ == "__main__":

    # 需要接收从unity传来的数据时，需要开一个线程，防止接收函数阻滞。

    # 轮椅直线运行实验时使用
    # recv_thread = threading.Thread(target=log_from_unity)
    # recv_thread.start()
    # wheelchair_run_straight("COM5")

    # 轮椅调试运行时使用
    # recv_thread = threading.Thread(target=log_from_unity)
    # recv_thread.start()
    # wheelchair_debug("COM5", 2, 0.2)

    # 接收轮椅相关串口数据时使用
    # recv_thread = threading.Thread(target=log_from_port)
    # recv_thread.start()
    # recv_from_port("COM5", out="out2")

    # 控制杆控制轮椅与unity轮椅时使用，udp传输
    # recv_thread = threading.Thread(target=log_from_unity)
    # recv_thread.start()
    # send_control_code_to_unity_udp("COM5", out="out2")

    # 控制杆控制轮椅与unity轮椅时使用，tcp传输
    send_control_code_to_unity_tcp("COM5", out="out2")
