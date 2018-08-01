from tools import vkapi
from settings import *
from tools.log import logger
from tools.exceptions import ManualException
from db.mymodels import *
from sender.Sender import Sender
from peewee import fn
import traceback
import re


class BotBase:
    def __init__(self, token):
        self._bad_message = 'Простите, во время работы произошли неполадки. Повторите запрос позже.'
        self._token = token
        self._sender = Sender()
        self._wait_for_sender = list() # лист тех, от кого ожидается токен, чтобы добавить их страницу, как рассыльщика
        self._wait_for_moderators = {} # аналогично, только для тех, кто добавляет группу

    def reply_to_message(self, data):
        logger.info('call "bot.reply_to_message')
        user_id = data['object']['user_id']

        logger.info('USERID: '+ str(user_id))
        print('After USERID, moderators: ', end='')
        print(self._wait_for_moderators)


        # TODO производить удаления пользователей при добавлении в другие категории (Юзер -> админ)
        try:
            if user_id in self._wait_for_moderators:

                logger.info('Group moderator sended url with access token.')
                self._add_group(self._wait_for_moderators[user_id], user_id, data)

                logger.info('before send_message')
                self.send_message(user_id, 'Группа добавлена.')

                del self._wait_for_moderators[user_id]

            elif user_id in self._wait_for_sender:
                # страница-рассыльщик прислала ссылку с токеном

                logger.info('Sender sended url with access token.')

                message = data['object']['body']

                access_token = vkapi.get_access_token_from_url(message)

                sender = SenderPage.create(vkid=user_id, token=access_token, message_count=self._sender._message_limit)
                self._sender.something_is_changed()

                logger.info('wait_for_sender: ' + str(self._wait_for_sender))
                self._wait_for_sender.remove(user_id)

                self.send_message(user_id, 'Я добавил эту страницу.')

            elif AdminPage.select().where(AdminPage.vkid == user_id).exists():
                self.send_message(user_id, self.reply_to_admin(data))

            elif UserPage.select().where(UserPage.vkid == user_id).exists():
                # если страница пользователя прислала ответ
                self._receive_user_response(data)

            else:
                logger.info('Random user sended to me a message.')

                random_query = AdminPage.select().order_by(fn.Random())

                # tgroup = TargetGroup.get(TargetGroup.admin_id == random_admin.vkid)
                # new_user = UserPage.create(vkid=user_id, target_group=tgroup, status='active') # TODO check

                if random_query.exists():
                    random_admin = random_query.get()
                    vkapi.forward_messages(random_admin.vkid, token=self._token,
                                       messages_id=str(data['object']['id']))

        except ManualException as ex:
            vkapi.send_message(user_id=user_id, token=self._token, message=ex.message)
        except Exception as ex:
            vkapi.send_message(user_id=user_id, token=self._token, message=self._bad_message)
            raise ex

        return 'ok'

    def _receive_user_response(self, data):
        user_id = data['object']['user_id']

        logger.info('User page sended respose.')

        user = UserPage.get(UserPage.vkid == user_id)
        user.status = 'active'  # пользователь откликнулся

        tgroup = user.target_group
        admin_vkid = AdminPage.select().where(AdminPage.vkid == tgroup.admin_id).get().vkid

        vkapi.forward_messages(admin_vkid, token=self._token,
                               messages_id=str(data['object']['id']))

        user.save()

    def reply_to_admin(self, data):
        logger.info('in reply_to_admin()')

        message = data['object']['body'].lower()
        user_id = data['object']['user_id']

        try:
            if message.find('добавь админа') != -1 or message.find('добавить админа') != -1:
                self._add_admin(message)
                return 'Админ добавлен.'

            elif message.find('добавь группу') != -1 or message.find('добавить группу') != -1: #TODO change find to [a, b]
                # self._add_group(user_id, message)

                self._wait_for_moderators[user_id] =  vkapi.message_to_vkid(message) # будем ждать ответа

                print(self._wait_for_moderators)

                return self._get_mess_with_auth_link()

            elif message[:15] == 'колво сообщений':
                self._change_mess_count(message)
                return 'Количество сообщений изменено.'

            elif message[:5] == 'текст': # TODO text для конкретной группы
                self._change_text(data['object']['body']) # неизмененный текст нужен
                return 'Текст изменен.'

            elif message[:24].find('добавь страницу') != -1 or message[:24].find('добавить страницу') != -1:
                return self._add_sender(user_id, message)

            elif message[:16].find('запусти рассылку') != -1 or message[:16].find('запустить рассылку') != -1:
                self._sender.run()
                return 'Рассылка запущена.'

            elif message[:20].find('останови рассылку') != -1 or message[:20].find('остановить рассылку') != -1:
                self._sender.stop()
                return 'Рассылка остановлена.'

            else:
                return 'Я не понял команды. Попробуйте еще раз.'

        except ManualException as ex:
            logger.info('EXCEPTION RAISED: ' + ex.message)
            return ex.message
        except Exception as ex:
            logger.info('EXCEPTION RAISED: ' + str(ex))
            traceback.print_exc()
            return self._bad_message

    def _add_admin(self, message):
        logger.info('in BotBase._add_admin()')

        new_anmin_vkid = vkapi.message_to_vkid(message)

        admin = AdminPage.create(vkid=new_anmin_vkid, target_group=None)

    def _add_group(self, group_id, moderator_id, data):
        message = data['object']['body']

        self._sender.something_is_changed()
        logger.info('in BotBase._add_group()')

        group_members = vkapi.get_group_memb(group_id, vkapi.get_access_token_from_url(message))

        # TODO ТУТ КОСТЫЛЬ
        tg_group = TargetGroup.create(id=1, vkid=group_id, admin_id=moderator_id, text='', message_count=0)

        logger.info('Before circle')
        for user in group_members:
            print(user)
            # проверка, что этот пользователь не админ
            if not AdminPage.select().where(AdminPage.vkid == user).exists():
                user_page = UserPage.create(vkid=user, target_group=tg_group, status='not noticed')
                user_page.save()

        logger.info('After circle')


    def _change_mess_count(self, message):
        self._sender.something_is_changed()
        logger.info('in BotBase._change_mess_count()')

        without_mes_count = message.split()
        without_mes_count.pop() # выкидывает количество сообщений

        group_id = vkapi.message_to_vkid(without_mes_count[-1]) # кидает внутрь последнее слово
        group = TargetGroup.get(TargetGroup.vkid == group_id)
        group.message_count = message.split()[-1]
        group.save()

    def _change_text(self, message):
        self._sender.something_is_changed()
        text = re.findall('\"[\w\W]*\"', message)[0] # берет текст
        request = message.replace(' ' + text, '')
        group_id = vkapi.message_to_vkid(request)

        text = text[1:-1] # отрезает ковычки

        group = TargetGroup.get(TargetGroup.vkid == group_id)
        group.text = text
        group.save()

    def _add_sender(self, user_to_response, message):
        response = 'Я отправил запрос к {0}. ' \
                   'Необходимо зайти на эту страницу и подтвердить добавление.'.format(vkapi.message_to_vkid(message))



        vkapi.send_message(vkapi.message_to_vkid(message), self._token,
                           'Вашу страницу добавляют для рассылки, '
                           'для подтверждения этого надо пройти по этой ссылке {0}, '
                           'скопировать ссылку из адресной строки и отправить мне обратно.'
                           .format(vkapi.auth_link))

        logger.info('Added to _wait_for_sender {0}'.format(vkapi.message_to_scrname(message)))
        self._wait_for_sender.append(vkapi.message_to_vkid(message))

        return response

    def _get_mess_with_auth_link(self):
        return 'Перейдите по ссылке и разрешите доступ к странице. ' \
                   'После этого необходимо ссылку из браузера скопировать и прислать мне. Ссылка: ' + vkapi.auth_link

    def send_message(self, user_id, message):
        print(message)
        # vkapi.send_message(user_id, self._token, message)



