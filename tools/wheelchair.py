import datetime
import serial

global ser
global recv_data


def port_init(port):
    """
    串口初始化函数，开启串口port，波特率115200，数据位8位，停止位1位

    :param port: 串口端口号
    :return: serial.Serial类ser
    """

    global ser
    try:
        ser = serial.Serial(port=port, baudrate=115200, bytesize=8, stopbits=1,
                            timeout=0.1, write_timeout=0.1, inter_byte_timeout=0.1)
        ser.set_buffer_size(rx_size=1024, tx_size=1024)
        print("串口{}打开成功！！".format(port))

    except:
        print("串口{}打开失败，请检查串口号！！RS232是否连接！！".format(port))

    return ser


def motor_code(Dir, true_speed):
    """
    一个电机控制码转换函数，输入使能EN，方向Dir，电机速度true_speed

    Parameters
    ----------
    :param Dir: 逆时针转：0，顺时针转：1
    :param true_speed: 电机运行速度
    :return: 单个电机的控制码，需要输入到motor_full_code()中输出完整控制码使用
    """

    if true_speed != 0:
        EN = 1
    else:
        EN = 0

    # speed = int(true_speed * 219.8)  # 速度转换
    speed = int(true_speed * 219.8 * 0.75)  # 速度转换与修正

    speed_up_4_bit = (0xf0 & speed) >> 4
    speed_low_4_bit = 0x0f & speed

    speed_data = [0 for i in range(3)]

    speed_data[0] = 0x30 | EN | (Dir << 1)

    speed_data[1] = 0x30 | speed_up_4_bit
    speed_data[2] = 0x30 | speed_low_4_bit

    return speed_data


def other_output(out: str):
    """
    输入需要从轮椅串口读出的数据类别，本函数转换成相应的控制码。

    :param out: 数据类别：详情请查看通讯协议
    :return: 控制码
    """

    output_code = [0 for i in range(2)]

    if out == "out2":
        output_code = [0x34, 0x30]  # 0011 0100, 0011 0000
    elif out == "out3":
        output_code = [0x38, 0x30]  # 0011 1000, 0011 0000
    elif out == "out4":
        output_code = [0x30, 0x31]  # 0011 0000, 0011 0001
    elif out == "out5":
        output_code = [0x30, 0x32]  # 0011 0000, 0011 0010
    elif out == "out6":
        output_code = [0x30, 0x34]  # 0011 0000, 0011 0100
    elif out == "out7":
        output_code = [0x30, 0x38]  # 0011 0000, 0011 1000
    elif out == "Table DOWN":
        output_code = [0x32, 0x30]  # 0011 0010, 0011 0000
    elif out == "Table UP":
        output_code = [0x32, 0x31]  # 0011 0001, 0011 0000
    elif out == "None":
        output_code = [0x30, 0x30]  # 0011 0000, 0011 0000
    else:
        print("请正确输入需要从串口读出的数据类型out2~0ut7，或扶手板动作Table DOWN or Table UP！！")

    return output_code


def motor_full_code(FL_motor, FR_motor, BL_motor, BR_motor, out="None"):
    """
    轮椅控制码输出函数，输入四个电机的单独控制码，拼接成完整控制码输出。
   FL_motor------FR_motor
      |           |
   BL_motor------BR_motor

    0逆1顺

    轮椅前进：
    0逆------1顺
     |        |
    0逆------1顺

    Parameters
    ----------
    :param FL_motor: 左前电机控制码
    :param FR_motor: 右前电机控制码
    :param BL_motor: 左后电机控制码
    :param BR_motor: 右后电机控制码
    :param out: 需要从串口读出的数据
    :return: 轮椅完整控制码
    """

    full_code = [0 for i in range(21)]
    full_code[0] = 0x01

    full_code[1] = FL_motor[0]
    full_code[2] = FL_motor[1]
    full_code[3] = FL_motor[2]

    full_code[4] = FR_motor[0]
    full_code[5] = FR_motor[1]
    full_code[6] = FR_motor[2]

    full_code[7] = BL_motor[0]
    full_code[8] = BL_motor[1]
    full_code[9] = BL_motor[2]

    full_code[10] = BR_motor[0]
    full_code[11] = BR_motor[1]
    full_code[12] = BR_motor[2]

    # full_code[13] = 0x30
    # full_code[14] = 0x30

    other_output_code = other_output(out=out)
    full_code[13] = other_output_code[0]
    full_code[14] = other_output_code[1]

    full_code[15] = 0x30
    full_code[16] = 0x30

    FCS = 0
    for i in range(17):
        FCS ^= full_code[i]

    full_code[17] = 0x30 | (FCS & 0xf0) >> 4
    full_code[18] = 0x30 | (FCS & 0x0f)

    full_code[19] = 0x0d
    full_code[20] = 0x0a

    return full_code


def port_send_data(data, wheelchair_serial, true_speed):
    """
    向串口输出控制码，控制轮椅运行。

    Parameters
    ----------
    :param data: 控制码
    :param wheelchair_serial:port_init()函数初始化的serial.Serial类ser
    :param true_speed: 轮椅运行速度
    :return: 无
    """
    wheelchair_serial.write(data)
    if true_speed != 0:
        print("2--true_speed = {}".format(true_speed))
    wheelchair_serial.flush()


def forward_straight_moving(true_speed):
    """
    轮椅直线向前运动函数。此函数主要应用到轮椅自动直线运行时诱发人的情绪，只会向串口发送电机控制指令，不接收串口数据。

    Parameters
    ----------
    :param true_speed: 轮椅运行速度
    :return: 轮椅控制码，需要借助port_send_data()函数输出
    """
    FL_motor = motor_code(0, true_speed)  # 0逆1顺
    FR_motor = motor_code(1, true_speed * 1.025)  # 轮椅直线前进时由于某些原因，方向会向右偏，给右前轮一个修正速度
    BL_motor = motor_code(0, true_speed)
    BR_motor = motor_code(1, true_speed)
    full_code = motor_full_code(FL_motor, FR_motor, BL_motor, BR_motor, out="None")

    return full_code


def recv_data_init(serial, out="None"):
    """
    初始化接收数据，根据通讯协议，先向串口发送一个控制码，然后从串口接收数据。

    :param serial: 串口端口号
    :param out: 需要接收的数据类型
    :return: 无
    """
    FL_motor = motor_code(0, 0)  # 0逆1顺
    FR_motor = motor_code(1, 0)
    BL_motor = motor_code(0, 0)
    BR_motor = motor_code(1, 0)
    full_code = motor_full_code(FL_motor, FR_motor, BL_motor, BR_motor, out=out)
    port_send_data(full_code, serial, 0)


def log_from_port(receive_data):
    """
    从串口接收到的数据存入日志文件

    :param receive_data: 接收到的数据
    :return:无
    """

    with open("./log/recvdata_log.txt", "a") as unity_log:
        # unity_log.write(str(datetime.datetime.now()) + "\t" + str(receive_data) + "\n")
        unity_log.write(datetime.datetime.now().strftime("%m-%d %H:%M:%S") + "\t" + str(receive_data) + "\n")
    unity_log.close()


# def log_from_port():
#     """
#     从串口接收到的数据存入日志文件
#
#     :param receive_data: 接收到的数据
#     :return:
#     """
#
#     global recv_data
#
#     with open("./log/recvdata_log.txt", "a") as unity_log:
#         unity_log.write(str(datetime.datetime.now()) + "\t" + str(recv_data) + "\n")
#     unity_log.close()
