from db.mymodels import *
from enum import Enum
from tools import vkapi
from tools.log import logger
from datetime import timedelta

class State(Enum):
    stopped = 1
    waiting = 2
    rerun = 3
    active = 4


class Sender:
    def __init__(self):
        self._state = State.stopped
        self._message_limit = 20

    def run(self):
        self._state = State.active

        self._send_messages()
        while self._state == State.rerun:
            self._update_mess_count()
            self._update_group_memb()

            self._send_messages()

        self._state = State.waiting

    def _update_mess_count(self):
        not_updated = SenderPage.get(SenderPage.update_time <= datetime.now())

        for sendr in not_updated:
            sendr.message_count = self._message_limit
            sendr.update_time = datetime.now() + timedelta(hours=12, minutes=10)

    def _update_group_memb(self):
        groups = TargetGroup.select(TargetGroup.vkid)

        for group in groups:
            members = vkapi.get_group_memb(group.vkid)

            for member in members:
                query = UserPage.select().where(UserPage.vkid == member)
                if not query.exists():
                    new_member = UserPage(vkid=member, target_group=group, status='not noticed')
                    new_member.save()
                else:
                    break

    def _send_messages(self):
        users = UserPage.select()

        if users.exists():
            sender_query = SenderPage.select().where(SenderPage.message_count != 0)

            if sender_query.exists():
                sender = sender_query.get()

                for user in users:
                    self.send_message(sender.token, user.vkid, user.target_group.text)

                    sender.message_count -= 1
                    if sender.message_count == 0:
                        sender.save()
                        sender_query = SenderPage.select().where(SenderPage.message_count != 0)

                        if not sender_query.exists():
                            return

                        sender = sender_query.get()

                sender.save()

    def send_message(self, from_token, to_id, message):
        logger.info('send \"' + str(message) + ' \" from ' + str(from_token) + ' to ' + str(to_id))
        vkapi.send_message(user_id=to_id, token=from_token, message=message)

    def something_is_changed(self):
        if self._state != State.stopped:
            self._state = State.rerun

