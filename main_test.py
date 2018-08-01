from db.mymodels import *
from flask import Flask, json, request, g
from app import app
from db.creating_scratch import create_db
from tools.log import logger
from tools.debug import setDEBUG


@app.route('/test', methods=['GET'])
def test():
    # for i in dir(tests):
    #     item = getattr(tests,i)
    #     if callable(item):
    #         item()

    import tests.server_tests as tests

    g.db.drop_tables([AdminPage, TargetGroup, UserPage, SenderPage], safe=True) # TODO delete it
    create_db()

    for i in dir(tests):
        item = getattr(tests,i)
        if callable(item) and repr(item).find('test_') != -1:
            print(repr(item))
            item()

    logger.info('All tests are passed!')
    return 'ok'