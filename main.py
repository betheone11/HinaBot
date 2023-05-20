# -*- coding:utf-8 -*-
import logging
from typing import List

from pycqBot.data import *

from HnHttpApi import HnHttpApi, HinaBot
from HinaBot import HinaBot
from pycqBot.cqHttpApi import cqHttpApi, cqLog


def save(command_data, message: Message) -> None:
    """
    输入：类别-标题-内容
    """
    message.reply('开始存储数据，请输入 类别-标题-内容 格式的文本！')
    data = hqapi.reply(message.sender.id, 20)
    # 为空说明超时了也没进行输入
    if data is None:
        message.reply("超过等待时间！")
        return
    try:
        class_, key, values = data.raw_message.split('-')
        print(class_, '+', key, '+', values)
        hqapi.recording_message(data, class_, key, values)
        data.reply('存储成功')
    except Exception as err:
        logging.error(err)


def list_keys(command_data, message: Message) -> None:
    # todo: 不要回复，而是直接发送信息
    _, class_ = message.raw_message.split(' ')
    message_list = hqapi.list_keys(message, class_)
    if not message_list:
        return
    for keys in message_list:
        message.reply('%s' % keys)


if __name__ == '__main__':
    # cqapi = cqHttpApi()
    hqapi = HnHttpApi()
    bot = hqapi.create_bot(host='ws://127.0.0.1:8000', options={
        "messageSql": True
    })
    bot.command(save, '存储', {
        'help': ['/存储：存储信息，以 类别-关键字-信息 的格式输入'],
        'type': 'all'
    })
    bot.command(list_keys, '列出所有关键字', {
        'help': ['/哈哈：列出指定类别的所有关键字'],
        'type': 'all'
    })
    cqLog()
    bot.start(go_cqhttp_path='go-cqhttp')
