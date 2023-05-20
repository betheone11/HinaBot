import logging
import os
import sqlite3
import time
from typing import Any, Optional
from pycqBot.data import *

from pycqBot.cqHttpApi import cqHttpApi, cqBot

ALL_CLASS = ['LearningResources', 'Notice', 'Entertainment', 'ComputerAccessories']


class HnHttpApi(cqHttpApi):
    db_path = "./hbot_sql.db"

    def __init__(self):
        super().__init__()

    def create_bot(self, host: str = "ws://127.0.0.1:8080", group_id_list=None, user_id_list=None,
                   options=None) -> "HinaBot":
        """
        创造一个机器人
        """
        if options is None:
            options = {}
        if user_id_list is None:
            user_id_list = []
        if group_id_list is None:
            group_id_list = []

        return HinaBot(
            self, host, group_id_list, user_id_list, options
        )

    def create_tables(self, db_path: str, class_: str) -> None:
        """
        初始化表
        """
        if class_ not in ALL_CLASS:
            # todo 做一个错误处理
            pass
        # db_path = os.path.join(db_path, "hbot_sql.db")
        # self.db_path = db_path

        # if not os.path.isfile(db_path):
        #     os.remove(db_path)

        with sqlite3.connect(self.db_path) as con:
            sql_cursor = con.cursor()
            sql_cursor.execute(
                """CREATE TABLE IF NOT EXISTS '%s' (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Key NOT NULL,
                stime NOT NULL,
                userId NOT NULL,
                messageData TEXT NOT NULL
                );
                """ % class_
            )
            con.cursor()

    def recording_message(self, message: Message, class_: str, key: str, values: str) -> None:
        """
        永久存储信息
        """
        time_int = int(time.time())
        # try:
        print('实际打开路径：', self.db_path)
        with sqlite3.connect(self.db_path) as sql_link:
            sql_cursor = sql_link.cursor()
            sql_cursor.execute("""
            INSERT INTO %s VALUES (
                NULL, "%s", "%s", "%s", "%s"
            )
            """ % (class_, key, time_int, message.sender.id, values))
            sql_link.commit()
        # except Exception as err:
        #     logging.error(err)
        #     print('sql出错了！')

    def get_message(self, message: Message, class_: str, key: str) -> Optional[list[dict[str, Any]]]:
        """
        获取信息
        """
        try:
            with sqlite3.connect(self.db_path) as sql_link:
                sql_cursor = sql_link.cursor()
                data_cursor = sql_cursor.execute("""
                SELECT * FROM %s WHERE Key = '%s'
                """ % (class_, key))
            data_list = data_cursor.fetchall()
            return data_list

        except Exception as err:
            # todo 错误处理
            logging.error(err)
        return None

    def list_keys(self, message: Message, class_: str) -> Optional[list[dict[str, Any]]]:
        """
        列出指定表内的所有key
        """
        try:
            with sqlite3.connect(self.db_path) as sql_link:
                sql_cursor = sql_link.cursor()
                data_cursor = sql_cursor.execute("""
                SELECT Key FROM %s
                """ % class_)
            data_list = data_cursor.fetchall()
            return data_list

        except Exception as err:
            # todo 错误处理
            logging.error(err)
        return None

    def remove_message(self, message: Message, class_: str, key: str) -> bool:
        """
        删除指定表内信息
        """
        if self._thinking_twice(message):
            try:
                with sqlite3.connect(self.db_path) as sql_link:
                    sql_cursor = sql_link.cursor()
                    data_list = sql_cursor.execute("SELECT * FROM %s WHERE Key = '%s'" % (class_, key))
                    for data in data_list:
                        sql_cursor.execute("DELETE from %s WHERE ID = '%s'" % (class_, data[0]))
                    sql_link.commit()
                return True
            except Exception as err:
                self.recordMessageCKError(err)
                return False

    def _thinking_twice(self, message: Message) -> bool:
        """
        删除二次确认
        """
        try:
            message.reply('是否删除信息？（Y/N）')
            data = self.reply(message.sender.id, 20)
            print(data.message)
            print(data.message.lower())
            if data.message.lower() == 'y':
                return True
            return False
        except Exception as err:
            logging.error(err)
            return False

    def command_data_ck(self, command_data: str) -> list[str]:
        """
        去除命令中多余的空格
        """
        cked_data = [i for i in command_data if i != '']
        return cked_data


class HinaBot(cqBot):
    def __init__(self, hqapi: HnHttpApi, host: str = "ws://127.0.0.1:8080", group_id_list=None, user_id_list=None,
                 options=None):
        if options is None:
            options = {}
        if user_id_list is None:
            user_id_list = []
        if group_id_list is None:
            group_id_list = []
        super().__init__(hqapi, host, group_id_list, user_id_list)
        self.hqapi = HnHttpApi()
        # 指令标识符
        self.commandSign: str = '/'
        self.messageSql: bool = False
        # 长效消息存储 数据库目录

        for key in options.keys():
            if type(options[key]) is str:
                exec("self.%s = '%s'" % (key, options[key]))
            else:
                exec("self.%s = %s" % (key, options[key]))

    def meta_event_lifecycle_connect(self, event: Meta_Event):
        """
        连接响应
        """
        self.set_bot_status(event)
        if self.messageSql is True:
            for tables in ALL_CLASS:
                self.hqapi.create_tables(self.messageSqlPath, tables)
        logging.info("成功连接 websocket 服务! bot qq:%s" % self.__bot_qq)

    def set_bot_status(self, event: Meta_Event) -> None:
        self.__bot_qq = event.data["self_id"]
        self.hqapi.bot_qq = event.data["self_id"]
