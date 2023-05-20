import requests
from flask import Flask, request


def send(message):
    url = "http://127.0.0.1:5700/send_msg"  # 这里要加上http://，不然会报错
    data = request.get_json()  # 获取上报消息
    params = {
        "message_type": data['message_type'],
        "group_id": data['group_id'],
        "message": message
    }
    requests.get(url, params=params)

def messagex():
    data = request.get_json()
    message = data['message']
    if "你好" == message:
        send("阿草在哦")
    else:
        print("指令错误")  # 这里不是发送，是打印到我们后台监听程序
