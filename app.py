from flask import Flask, json, request
# import os
# import urllib.parse as urlparse
# import psycopg2

# if 'HEROKU' in os.environ:
#     DEBUG = False
#     urlparse.uses_netloc.append('postgres')
#     url = urlparse.urlparse(os.environ['DATABASE_URL'])
#     DATABASE = {
#         'engine': 'peewee.PostgresqlDatabase',
#         'name': url.path[1:],
#         'user': url.username,
#         'password': url.password,
#         'host': url.hostname,
#         'port': url.port,
#     }
# else:
#     DEBUG = True
#     DATABASE = {
#         'engine': 'peewee.PostgresqlDatabase',
#         'name': 'framingappdb',
#         'user': 'postgres',
#         'password': 'postgres',
#         'host': 'localhost',
#         'port': 5432,
#         'threadlocals': True
#     }

app = Flask(__name__)
# app.config.from_object(__name__)