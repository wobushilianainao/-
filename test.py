import serial
import time

# 连接到Arduino的串口端口
arduino_port = 'COM7'  # 请根据您的实际端口进行修改
baud_rate = 9600  # 串口波特率，与Arduino代码一致

# 创建串口对象
arduino = serial.Serial(arduino_port, baud_rate, timeout=1)

# 等待Arduino初始化
time.sleep(2)


def send_command(command):
    # 发送单个字符命令到Arduino
    arduino.write(command.encode())

    # 等待Arduino处理命令
    time.sleep(1)

    # 获取Arduino的响应
    if arduino.in_waiting > 0:
        response = arduino.readline().decode('utf-8').strip()
        print("Arduino response:", response)

time.sleep(2)
# 示例控制：按顺序执行各项操作
send_command('0')  # 启动气泵并关闭电磁阀
time.sleep(3)  # 持续1500毫秒
send_command('1')  # 关闭气泵和电磁阀
time.sleep(3)  # 等待800毫秒
send_command('2')  # 关闭气泵和电磁阀
time.sleep(2)  # 等待800毫秒
# 关闭串口连接
arduino.close()
