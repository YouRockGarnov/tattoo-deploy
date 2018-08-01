from tools.debug_process import debug_processing
import vkbot_main
import tools.vkapi as vkapi
from db.mymodels import *
from sender.Sender import State
import time
from flask import g
import requests
from tools.log import logger

main_url = 'https://tattoo-sender.herokuapp.com'

def assertTrue(expr, funcname):
    if not expr:
        print('!! Not true in {0} !!!'.format(funcname))
        exit(1)

def assertEqual(a, b, funcname):
    if a != b:
        print('{0} != {1} in {2}!'.format(a, b, funcname))
        exit(1)

def make_req(message):
    response = requests.post(main_url, message.encode())

    if response != 200:
        logger.error('POST request to {0} with message = {1} returned {2}.'.format(main_url, message, response))
        exit(1)

def test_not_command_mes():
    g.db.close()

    debug_processing('{"type": "message_new", '
              '"object": {"id": 43, "date": 1492522323, "out": 0, '
              '"user_id": 142872618, "read_state": 0, "title": '
              '"Это тестовое сообщение", "body": "Пересланное"}}')

    assertEqual(vkapi.sended_message, 'Я не понял команды. Попробуйте еще раз.', __name__)

def test_add_admin(): # working
    g.db.close()

    query = AdminPage.select().where(AdminPage.vkid == 481116745)
    if query.exists():
        admin = query.get()
        admin.delete_instance()

    debug_processing('{"type": "message_new", "object": {"id": 43, "date": 1492522323, '
                                                                   '"out": 0, "user_id": 142872618, "read_state": 0, '
                                                                   '"body": "Добавь админа https://vk.com/id481116745"}}')

    query = AdminPage.select().where(AdminPage.vkid == 481116745)
    assertTrue(query.exists(), __name__)

    yuri = query.get()
    assertEqual(yuri.vkid, 481116745, __name__)

def test_add_group(): # working
    pass
    # TODO refact it
    # g.db.close()
    #
    # group_id = 168619478
    # query = TargetGroup.select().where(TargetGroup.vkid == group_id)
    #
    # if query.exists():
    #     group = query.get()
    #     users = UserPage.get(UserPage.target_group == group)
    #
    #     logger.info(users)
    #     users.delete_instance()
    #     group.delete_instance()
    #
    # debug_processing('{"type": "message_new", "object": {"id": 43, "date": 1492522323, '
    #                                                                '"out": 0, "user_id": 142872618, "read_state": 0, '
    #                                                                '"body": "Добавь группу https://vk.com/tatbottoo"}}')
    #
    # query = TargetGroup.select().where(TargetGroup.vkid == group_id)
    # assertTrue(query.exists(), __name__)
    #
    # tatbottoo = query.get()
    # assertEqual(tatbottoo.vkid, group_id, __name__)

def test_change_mess_count(): #working
    g.db.close()

    group_id = 168619478
    new_mes_count = 15

    query = TargetGroup.select().where(TargetGroup.vkid == group_id)
    assertTrue(query.exists(), __name__)

    debug_processing('{"type": "message_new", "object": {"id": 43, "date": 1492522323,'
                       '"out": 0, "user_id": 142872618, "read_state": 0,'
                       '"body": "колво сообщений у https://vk.com/tatbottoo ' + str(new_mes_count)
                        + '"}}')

    query = TargetGroup.select().where(TargetGroup.vkid == group_id)
    assertTrue(query.exists(), __name__)
    assertEqual(query.get().message_count, new_mes_count, __name__)

def test_add_sender():
    g.db.close()

    sender = 'patlin'
    sender_id = vkapi.to_vkid(sender)

    query = SenderPage.select().where(SenderPage.vkid == sender_id)

    if (query.exists()):
        inst = query.get()
        inst.delete_instance()

    assertTrue(not query.exists(), __name__)

    debug_processing('{"type": "message_new",'
                '"object": {"id": 43,'
                '"date": 1492522323,'
                '"out": 0, "user_id": 142872618, "read_state": 0,'
                '"body": "добавить страницу ' +
                str(sender) + '"}}')

    fake_token = 'https://oauth.vk.com/blank.html#access_token=f616432f6d3124e6e0fa29d45818848de94267c747ac20e3a4f5f90d00195da39d2d5f26d218f4211f538' \
                 '&expires_in=0&user_id=XXXXXXXXX&email=ya@www.pandoge.com'

    debug_processing('{"type": "message_new",'
                '"object": {"id": 43,'
                '"date": 1492522323,'
                '"out": 0, "user_id": 69337293, "read_state": 0,'
                '"body": "' + fake_token + '"}}')

    query = SenderPage.select().where(SenderPage.vkid == sender_id)
    assertTrue(query.exists(), __name__)

    sender = query.get()
    assertEqual(sender.vkid, sender_id, __name__)
    sender.delete_instance()

def test_change_text():
    g.db.close()

    group_id = 168619478
    new_text = 'Это новый текст. Ничего интересного.'

    query = TargetGroup.select().where(TargetGroup.vkid == group_id)
    assertTrue(query.exists(), __name__)

    debug_processing('{"type": "message_new", "object": {"id": 43, "date": 1492522323, '
                                   '"out": 0, "user_id": 142872618, "read_state": 0, '
                                   '"body": "Текст у https://vk.com/tatbottoo \\"' +
                                    str(new_text) + '\\""}}')

    query = TargetGroup.select().where(TargetGroup.vkid == group_id)
    assertTrue(query.exists(), __name__)
    assertEqual(query.get().text, new_text, __name__)

def test_run_sender():
    g.db.close()

    sender = 'patlin'
    sender_id = vkapi.to_vkid(sender)

    assertEqual(vkbot_main.vkbot._sender._state, State.stopped, __name__)

    debug_processing('{"type": "message_new", "object": {"id": 43, "date": 1492522323, '
                                                                   '"out": 0, "user_id": 142872618, "read_state": 0, '
                                                                   '"body": '
                                                                       '"запусти рассылку"}}')

    assertEqual(vkbot_main.vkbot._sender._state, State.waiting, __name__)


def test_consumer_reply():
    g.db.close()

    user = 'id280679710'
    user_id = vkapi.to_vkid(user)

    time.sleep(1)

    debug_processing('{"type": "message_new", "object": {"id": 43, "date": 280679710, '
                               '"out": 0, "user_id": ' + str(user_id) + ', "read_state": 0, '
                               '"body": "Ну окей, меня заинтересовал ваш тату-салон."}}')

    user_page = UserPage.get(UserPage.vkid == user_id)
    assertEqual(user_page.status, 'active', __name__)

def test_consumer_mess():
    g.db.close()

    screenname = 'https://vk.com/paulpalich'
    consumer_id = vkapi.message_to_vkid(screenname)

    debug_processing('{"type": "message_new", "object": {"id": 43, "date": 1492522323, '
                                               '"out": 0, "user_id": '
                                                + str(consumer_id) + ', "read_state": 0, '  
                                               '"body": "Это случайное сообщение от случайного чувака!!!"}}')

    assertTrue(UserPage.select().where(UserPage.vkid == consumer_id).exists(), __name__)
