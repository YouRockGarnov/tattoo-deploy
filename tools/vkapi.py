import vk
from tools.debug import getDEBUG
from tools.exceptions import ManualException
from tools.log import logger, logged
from configs.config_vkbot import token
import vk.exceptions

session = vk.Session()
api = vk.API(session, v=5.0)

sended_message = ''

_app_id_for_auth = '6630979' # для того, чтобы получать доступ к странице - нужна авторизация.
                             # Она производится через это приложение.
auth_link = '''https://oauth.vk.com/authorize?client_id={app_id}
                   &scope=photos,audio,video,docs,notes,pages,status,
                   offers,questions,wall,groups,messages,email,
                   notifications,stats,ads,offline,docs,pages,stats,
                   notifications&response_type=token '''.format(app_id=_app_id_for_auth)  # TODO INSERT CORRECT TOKEN


def send_message(user_id, token, message, attachment=""):
    logger.info('send \"' + message.encode().decode("utf-8",'replace') + ' \" to ' + str(user_id))

    print(getDEBUG())
    if (getDEBUG()):
        print(message)
        global sended_message
        sended_message = message
        # api.messages.send(access_token=token, user_id=str(user_id), message=message, attachment=attachment)
    else:
        api.messages.send(access_token=token, user_id=str(user_id), message=message, attachment=attachment)

def forward_messages(user_id, token, messages_id, message='', attachment=''):
    logger.info('send \"' + message.encode().decode("utf-8", 'replace') + ' \" to ' + str(user_id))
    if (getDEBUG()):
        print(message)
        global sended_message
        sended_message = message
        # api.messages.send(access_token=token, user_id=str(user_id), message=message, attachment=attachment)
    else:
        api.messages.send(forward_messages=messages_id, access_token=token,
                          user_id=str(user_id), message=message, attachment=attachment)

def to_vkid(scr_name):
    if getDEBUG():
        if scr_name == 'thrash_yura':
            return 142872618
        elif scr_name == 'konstantinleladze':
            return 209780589
        elif scr_name == 'paulpalich':
            return 159817977
        elif scr_name == 'id481116745':
            return 481116745
        elif scr_name == 'patlin':
            return 69337293
        elif scr_name == 'tatbottoo':
            return 168619478
        elif scr_name == 'id280679710':
            return 280679710

    print(scr_name)

    response = api.utils.resolveScreenName(screen_name=scr_name, access_token=token)

    if response == []:
        raise ManualException('Кажется вы дали неверную ссылку, я не нашел такого пользователя!')
    # elif response['type'] != 'user':
    #     raise ManualException('Вы прислали ссылку не на пользователя. Админом может быть только пользователь.')
    # надо делать проверку в методах добавления админа

    return response['object_id']

@logged
def get_group_memb(group_id, moderator_token):
    if getDEBUG():
        return [159817977, 481116745, 280679710]

    # response = api.utils.resolveScreenName(screen_name=scr_name, access_token=token)
    # if response['type'] != 'group':
    #     raise ManualException('Данная ссылка не является ссылкой на группу!')



    try:
        return api.groups.getMembers(group_id=group_id, sort='time_desc', access_token=moderator_token)['users']
    except vk.exceptions.VkAPIError as ex:
        if str(ex).find('Access denied: you should be group moderator.') != -1:
            raise ManualException('Отклонено. Вы должны являться модератором сообщества, которое добавляете.')
        else:
            raise ex



def message_to_scrname(mess):
    return mess.split()[-1].split('/')[-1]

def message_to_vkid(mess):
    return to_vkid(message_to_scrname(mess))

def get_access_token_from_url(url):
    try:
        return url.split('access_token=')[1].split('&')[0]
    except Exception as ex:
        if str(ex).find('list index out of range') != -1:
            raise ManualException('Вы прислали неверную ссылку, попробуйте еще раз.')