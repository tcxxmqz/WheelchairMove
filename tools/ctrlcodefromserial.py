def control_code(recv_data):
    """
    串口数据传入此函数，传出控制指令字符串。
    例如：传入b'1_OP:0,2,2,0,0,1\r\n'，解析出('R', '右旋')

    :param recv_data: 串口接收到的二进制数据
    :return: 传送到unity的控制码，以及中文控制码，返回的是元组
    """
    if recv_data != b'':
        recv_data_code = []
        for i in range(len(recv_data)):
            recv_data_code.append(chr(recv_data[i]))

        index_start = 0
        control_code = []
        for index, _code in enumerate(recv_data_code):
            if _code == ":":
                index_start = index
            if _code in ['0', '1', '2', '3', '4', '5']:
                if index > index_start:
                    control_code.append(_code)
        control_code_str = control_code[-3] + control_code[-2] + control_code[-1]

    else:
        control_code_str = "000"

    control = "null"
    operate = "无"

    if control_code_str == "000":
        control = "null"
        operate = "无操作"

    elif control_code_str == "010":
        control = "W"
        operate = "上"

    elif control_code_str == "020":
        control = "S"
        operate = "下"

    elif control_code_str == "200":
        control = "A"
        operate = "左"

    elif control_code_str == "100":
        control = "D"
        operate = "右"

    elif control_code_str == "110":
        control = "WD"
        operate = "右上"

    elif control_code_str == "210":
        control = "AW"
        operate = "左上"

    elif control_code_str == "220":
        control = "SA"
        operate = "左下"

    elif control_code_str == "120":
        control = "DS"
        operate = "右下"

    elif control_code_str == "001":
        control = "R"
        operate = "右旋"

    elif control_code_str == "002":
        control = "L"
        operate = "左旋"

    return control, operate


if __name__ == "__main__":
    a = b'1_OP:0,2,2,0,0,0\r\n'
    b = control_code(a)
    print(b)
