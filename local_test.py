from db.mymodels import *
from flask import Flask, json, request, g
from app import app
from db.creating_scratch import create_db
from tools.log import logger
from tools.debug import setDEBUG
from db.creating_scratch import init_db
from db.mymodels import db_proxy


def test():
    with app.app_context():
        init_db()
        g.db = db_proxy
        g.db.connect()

        import tests.server_tests as tests

        g.db.drop_tables([AdminPage, TargetGroup, UserPage, SenderPage], safe=True) # TODO delete it
        create_db()

        for i in dir(tests):
            item = getattr(tests,i)
            if callable(item) and repr(item).find('test_') != -1:
                print('Test' + repr(item) + ' started!')
                item()

                print('Test' + repr(item) + ' ended!')

        logger.info('All tests are passed!')
        return 'ok'

import os
if not ('HEROKU' in os.environ):
    print('unitests started')
    setDEBUG(True)
    test()
    print('unitests ended')