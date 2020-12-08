"""
虚拟现实环境情绪诱发平台-轮椅驱动程序-Python版本
程序接收从unity中传入的速度，将速度按照智能轮椅通讯协议转换后，数据输出到串口，驱动轮椅运行
2020-11-19 designed by 戚震
"""

from tools.wheelchair import *
from tools.udpfromunity import *
from time import sleep
import datetime
import threading

global recv_data


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
    wheelchair_serial = port_init(port)
    # recv_data_init(wheelchair_serial, out=out)

    while True:
        recv_data_init(wheelchair_serial, out=out)
        recv_data = wheelchair_serial.read_until()
        # print(datetime.datetime.now())
        print("recv_data = {}".format(recv_data))
        log_from_port(recv_data)
        sleep(0.09)


if __name__ == "__main__":
    # 需要接收从unity传来的数据时，需要开一个线程，防止接收函数阻滞。
    # recv_thread = threading.Thread(target=log_from_unity)
    # recv_thread.start()

    # wheelchair_run_straight("COM5")
    # wheelchair_debug("COM5", 2, 0.2)

    # recv_thread = threading.Thread(target=log_from_port())
    # recv_thread.start()

    recv_from_port("COM5", out="out2")
