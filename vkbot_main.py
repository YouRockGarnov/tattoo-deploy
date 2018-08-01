from flask import json, request
from configs.config_vkbot import *
from bots.vkbot import VKBot
from tools.log import logger
from configs.config_vkbot import token
from db.mymodels import db_proxy
import db.creating_scratch as creating_scratch
from db.creating_scratch import init_db
from app import app
from flask import g
import tools.debug as debug_module
from main_test import test

vkbot = VKBot(token)

@app.before_request
def before_request():
    init_db()
    g.db = db_proxy
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/setDEBUG_True', methods=['GET'])
def setDEBUG_True():
    debug_module.setDEBUG(True)
    return 'DEBUG = True'

@app.route('/setDEBUG_False', methods=['GET'])
def setDEBUG_False():
    debug_module.setDEBUG(False)
    return 'DEBUG = False'

@app.route('/getDEBUG_Flag', methods=['GET'])
def get_debug():
    print(debug_module.getDEBUG())
    return 'DEBUG = {0}'.format(debug_module.getDEBUG())


@app.route('/create_db', methods=['GET'])
def create_db():
    return creating_scratch.create_db()

@app.route('/reset_db', methods=['GET'])
def reset_db():
    return creating_scratch.reset_db()

@app.route('/', methods=['POST'])
def processing():
    if debug_module.getDEBUG():
        logger.info('Run in debug.')

    logger.info('in processing')

    bindata = request.data
    # logger.info('data = {0}'.format(bindata))

    data = json.loads(bindata)

    # Вконтакте в своих запросах всегда отправляет поле типа
    if 'type' not in data.keys():
        logger.info('not vk')
        return 'not vk'

    if data['type'] == 'confirmation':
        logger.info('confirmation')
        return confirmation_token

    elif data['type'] == 'message_new' or data['type'] == 'service_reply':
        logger.info('pulled message: ' + str(data['object']))

        vkbot.reply_to_message(data)
        return 'ok'

    return 'ok'

@app.after_request
def after_request(response):
    db_proxy.close()
    return response

import os
if not ('HEROKU' in os.environ):
    get_debug()

#print(debug_processing({"type":"message_new","object":{"id":43, "date":1492522323,
 #                       "out":0, "user_id":142872618, "read_state":0, "title":"Это тестовое сообщение", "body":"Пересланное"}}))
