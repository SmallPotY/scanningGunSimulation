# -*- coding:utf-8 -*-

from pynput.keyboard import Key, Controller
import socket
import qrcode
import winsound
import datetime

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
    winsound.PlaySound("PromptSound.wav", flags=1)
    keyboard.type(t)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)


SIZE = 1024
PORT = 9306
local_ip = get_host_ip()
ip_port = ('0.0.0.0', PORT)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(ip_port)
server_addr = '{}:{}'.format(local_ip, PORT)

print('服务已启动,服务地址: ', server_addr)
show_img(server_addr)

while True:
    data, client_addr = s.recvfrom(SIZE)
    text = data.decode('utf-8')
    if text == 'testConnection':
        print('连接成功... ip:', client_addr)
        s.sendto(b'connectionSucceeded', client_addr)
    else:
        print(datetime.datetime.now(), text)
        key_input(text)
        s.sendto(b'success', client_addr)

# s.close()


