# -*- coding:utf-8 -*-

from pynput.keyboard import Key, Controller
import socket
import qrcode
import os

keyboard = Controller()


def show_img(t):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(t)
    qr.make(fit=True)
    img = qr.make_image()
    img.save('code.png')
    img.show()


def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        tmp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        tmp_server.connect(('8.8.8.8', 80))
        ip = tmp_server.getsockname()[0]
    finally:
        tmp_server.close()
    return ip


def key_input(t):
    keyboard.type(t)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    os.system("PromptSound.wav")


SIZE = 1024
PORT = 9306
local_ip = get_host_ip()
ip_port = ('0.0.0.0', PORT)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # udp协议
s.bind(ip_port)
server_addr = '{}:{}'.format(local_ip, PORT)

print('服务已启动,服务地址: ', server_addr)
show_img(server_addr)

while True:
    data, client_addr = s.recvfrom(SIZE)
    text = data.decode('utf-8')
    # print('server收到的数据', text)
    key_input(text)
    # server.sendto(data.upper(), client_addr)

# s.close()
