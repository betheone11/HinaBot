'''
from pycqBot.cqHttpApi import cqLog, cqHttpApi
from pycqBot.data.message import Message
import logging
from pycqBot.cqCode import image

cqapi = cqHttpApi()

bot = cqapi.create_bot(host='ws://127.0.0.1:8000', options={
    "messageSql": True
})


def get(_, message: Message):
    # 获取该条消息发送用户 qq 存储的消息
    message_list = cqapi.record_message_get(message.id)
    message.reply("qq %s 存储了 %s 条消息 如有消息内容如下" % (message.id, len(message_list)))

    if not message_list:
        return
    for i in message_list:
        for k in i:
            print(k)
    message_data = ""
    for record_message_data in message_list:
        record_message_data = eval(record_message_data[-1])
        message_data = "%s%s\n" % (message_data, record_message_data["message"])

    message.reply(message_data)


def iset(_, message: Message):
    message.reply("等待时间！20s")

    # 等待该条消息发送用户 二次输入
    data = cqapi.reply(message.id, 20)
    print(message.raw_message)

    # 为空说明超时了也没进行输入
    if data is None:
        message.reply("超过等待时间！")
        return

    # 存储二次输入的消息
    # 存储时长 60 * 60 一小时
    data.record(60 * 60)


def show(_, message: Message):
    message_list = [
        # image("图片名", "图片url")
        message.reply("初音未来! %s" % image('mirai.jpg',
                                         'https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fc-ssl.duitang.com%2Fuploads%2Fblog%2F202104%2F11%2F20210411225037_21024.thumb.1000_0.jpg&refer=http%3A%2F%2Fc-ssl.duitang.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1684400989&t=7c2e704e330e12e8c5b2fb5cffad9265'))]


def stop(_, message: Message):
    message.reply('停止提供服务！')
    bot.stop()


cqLog(logging.INFO)
bot.command(get, "get")

bot.command(iset, "set").command(show, 'show').command(stop, 'stop')

bot.start()

'''
# -*- coding:utf-8 -*-
from pycqBot.cqHttpApi import cqHttpApi, cqLog
from pycqBot.data.message import Message
import logging


def echo(command_data, message: Message):
    message.reply(''.join(command_data))
    print(message.sender.id)
    print(message.message)


def save(command_data, message: Message) -> None:
    message.reply('开始存储数据，请输入 标题：内容 格式的文本！')
    data = cqapi.reply(message.sender.id, 20)
    # 为空说明超时了也没进行输入
    if data is None:
        message.reply("超过等待时间！")
        return
    print(data.message)
    print(data.raw_message)

    # 存储二次输入的消息
    # 存储时长 60 * 60 一小时
    data.record(60 * 60)
    data.reply('该消息已存储')


def search(command_data, message: Message) -> None:
    message_list = cqapi.record_message_get(message.sender.id)
    message.reply("qq %s 存储了 %s 条消息 如有消息内容如下" % (message.sender.id, len(message_list)))
    if not message_list:
        return
    #  print("meaaage_list:",message_list[-1][-1])
    message_data = ""
    for record_message_data in message_list:
        record_message_data = eval(record_message_data[-1])
        message_data = "%s%s\n" % (message_data, record_message_data["message"])

    message.reply(message_data)


if __name__ == '__main__':
    cqapi = cqHttpApi()
    bot = cqapi.create_bot(host='ws://127.0.0.1:8000', options={
        "messageSql": True
    })
    bot.command(echo, 'echo', {
        'help': ['#echo - 你说啥我说啥'],
        'type': 'all'
    }).command(save, 'save', {
        'help': ['存储信息啦'],
        'type': 'all',
    }).command(search, 'search', {
        'help': ['查询信息！'],
        'type': 'all',
    })
    cqLog()
    bot.start(start_go_cqhttp=True, go_cqhttp_path='go-cqhttp')

