from bots.bot_base import BotBase
import configs.config_vkbot as config
import tools.vkapi as vkapi
from tools.log import logger
from db.mymodels import db_proxy


class VKBot(BotBase):
    def __init__(self, token):
        super().__init__(token)
        self._message_limit = 20
        # db.connect()

    def send_message(self, user_id, message):
        vkapi.send_message(user_id, self._token, message)


def return_all_atr(data):
    mess = list()
    for item in data['object'].values():
        mess.append(item)

    return mess
