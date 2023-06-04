# -*- coding:utf-8 -*-
import logging
from typing import List
from pycqBot.data import *
from HnHttpApi import HnHttpApi, HinaBot
from pycqBot.cqHttpApi import cqHttpApi, cqLog


class Echo:
    @staticmethod
    def echo(command_data, message: Message):
        message.reply(''.join(command_data))
        print(message.sender.id)
        print(message.message)
        print(command_data)
        command_data = hqapi.command_data_ck(command_data)
        print(command_data)


class InfoStorage:
    @staticmethod
    def save(command_data, message: Message) -> None:
        """
        输入：类别 标题 内容
        """
        message.reply('开始存储数据，请输入 类别 标题-内容-格式的文本！')
        data = hqapi.reply(message.sender.id, 120)
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

    @staticmethod
    def list_keys(command_data, message: Message) -> None:
        """
        列出指定表所有索引
        /命令 class_, key
        """
        class_ = command_data[0]
        message_list = hqapi.list_keys(message, class_)
        if not message_list:
            return
        print(message_list)
        send_message = ''
        for keys in message_list:
            send_message += keys[0] + '、'
        message.reply_not_code(send_message)

    @staticmethod
    def search_by_key(command_data, message: Message) -> None:
        """
        通过键查询
        /cmd class_ key
        """
        command_data = hqapi.command_data_ck(command_data)
        class_, key = command_data
        message_list = hqapi.get_message(message, class_, key)
        send_message = ''
        try:
            for row_msg in message_list:
                send_message += '：'.join([row_msg[1], row_msg[4]]) + '\n'
            send_message = send_message.rsplit('\n', 1)[0]
            message.reply_not_code(send_message)
        except Exception as err:
            logging.error(err)

    @staticmethod
    def remove_rcd_msg(command_data, message: Message) -> None:
        command_data = hqapi.command_data_ck(command_data)
        class_, key = command_data
        if hqapi.remove_message(message, class_, key):
            message.reply('删除成功')
            return
        message.reply('删除失败')


if __name__ == '__main__':
    # cqapi = cqHttpApi()
    hqapi = HnHttpApi()
    bot = hqapi.create_bot(host='ws://127.0.0.1:8000', options={
        "messageSql": True
    }).command(InfoStorage.save, '存储', {
        'help': ['/存储：存储信息，以 类别-关键字-信息 的格式输入'],
        'type': 'all'
    }).command(InfoStorage.list_keys, '列出关键字', {
        'help': ['/列出关键字：列出指定类别的所有关键字'],
        'type': 'all'
    }).command(InfoStorage.search_by_key, '键查询', {
        'help': ['/键查询：/键查询 类别 键 '],
        'type': 'all'
    }).command(Echo.echo, 'echo', {
        'type': 'all'
    }).command(InfoStorage.remove_rcd_msg, '删除', {
        'help': ['/删除 表名 键 # 删除表中的值'],
        'type': 'all'
    })
    cqLog(logging.INFO)
    bot.start(go_cqhttp_path='go-cqhttp')
