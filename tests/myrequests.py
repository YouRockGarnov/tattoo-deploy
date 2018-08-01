# def test():
#     print(debug_processing({'object': {'user_id': 'user_id', 'body': 'login password'}, 'type': 'message_new'}))
#     print(debug_processing({'object': {'user_id': 'user_id', 'success': 'True', 'title': 'hamta@yandex.ru'}, 'type': 'service_reply'}))
#     #print(processing({'object': {'user_id': 'user_id', 'title': 'Заголовок', 'body': [{'body': 'Первое пересланное сообщение'},
#     #                                                            {'body': 'Второе пересланное сообщение'}]}, 'type': 'message_new'}))
#     print(debug_processing({'type': 'message_new', 'object': {'user_id': 'user_id', 'title': 'Title'}}))
#
# # @app.route('/', methods=['POST'])
# def debug_processing(data):
#     # Распаковываем json из пришедшего POST-запроса
#
#     print('processing')
#
#     if DEBUG:
#         logger.info('Run in debug')
#     else:
#         data = json.loads(request.data)
#     # Вконтакте в своих запросах всегда отправляет поле типа
#
#     if 'type' not in data.keys():
#         return 'not vk'
#
#     if data['type'] == 'confirmation':
#         return confirmation_token
#
#     elif data['type'] == 'message_new' or data['type'] == 'service_reply':
#         logger.info('pulled message: ' + str(data['object']))
#
#         vkbot.reply_to_message(data)
#         return 'ok'
#
#     return 'ok'
#
# test()