# -*-coding:GBK-*-
import socket

global tcpSockets
global tcpLogSockets
global severIP


def log_from_unity_tcp(severIP):
    """
    ����unityͨ��tcp���ص���Ϣ�����浽��־�ļ���

    :param severIP: unity�˵ķ�������ַ
    :return:
    """
    with open("./log/unity_log.txt", "a") as unity_log:
        unity_log.write("ϵͳʱ��\t����ʱ��\t�ϰ������\t��ǰ�ٶ�" + "\n"
                        + "ϵͳʱ��\t����ʱ��\t����λ��\t����\n")
    unity_log.close()

    tcpLogSockets = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # ���ͻ��˵�ַ
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
