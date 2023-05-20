import logging

from pycqBot.cqHttpApi import cqBot, cqHttpApi
from typing import Union

from pycqBot.data import Meta_Event

ALL_CLASS = ['LearningResources', 'Notice', 'Entertainment', 'ComputerAccessories']


class HinaBot(cqBot):
    def __init__(self, cqapi: cqHttpApi, host: str = "ws://127.0.0.1:8080", group_id_list=None, user_id_list=None,
                 options=None):
        if options is None:
            options = {}
        if user_id_list is None:
            user_id_list = []
        if group_id_list is None:
            group_id_list = []
        super().__init__(cqapi, host, group_id_list, user_id_list)
        self.hqapi = HnHttpApi()
        # 指令标识符
        self.commandSign: str = '/'

    def meta_event_lifecycle_connect(self, event: Meta_Event):
        """
        连接响应
        """
        self.set_bot_status(event)
        if self.messageSql is True:
            for tables in ALL_CLASS:
                self.hqapi.create_tables(self.messageSqlPath, tables)

        logging.info("成功连接 websocket 服务! bot qq:%s" % self.__bot_qq)
