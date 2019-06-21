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


def key_input(t):
    winsound.Beep(800, 200)
    keyboard.type(t)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)


SIZE = 1024
PORT = 9306

ip_port = ('0.0.0.0', PORT)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(ip_port)

print('服务已启动... ')
print('当前主机名称:', socket.gethostname())
print('端口号:', PORT)

addr = socket.getaddrinfo(socket.gethostname(), None)
print('当前主机存在以下IP地址')
for item in addr:
    if ':' not in item[4][0]:
        print('=>' + item[4][0])

print('请选择与手机网段相同的IP连接...')
while True:
    data, client_addr = s.recvfrom(SIZE)
    text = data.decode('utf-8')
    if text == 'testConnection':
        print('收到测试连接请求, 请求地址:', client_addr)
        s.sendto(b'connectionSucceeded', client_addr)
    else:
        print(datetime.datetime.now(), '=>', text)
        key_input(text)
        s.sendto(text.encode('utf-8'), client_addr)

# s.close()
