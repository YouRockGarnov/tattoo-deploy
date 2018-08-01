from peewee import PostgresqlDatabase, Database, Proxy, SqliteDatabase
from db.mymodels import AdminPage, TargetGroup, UserPage, SenderPage
from db.mymodels import db_proxy

def init_db():
    import os
    if ('HEROKU' in os.environ):
        import urllib.parse as urlparse, psycopg2, os
        urlparse.uses_netloc.append('postgres')
        url = urlparse.urlparse(os.environ["DATABASE_URL"])
        db = PostgresqlDatabase(database=url.path[1:], user=url.username, password=url.password, host=url.hostname,
                                port=url.port)
        db_proxy.initialize(db)
    else:
        db = SqliteDatabase('sender.sqlite')
        db_proxy.initialize(db)

def create_db():
    import os
    if not ('HEROKU' in os.environ):
        db = SqliteDatabase('../sender.sqlite')
        db.connect(True)

        db.drop_tables([AdminPage, TargetGroup, UserPage, SenderPage])
        db.create_tables([AdminPage, TargetGroup, UserPage, SenderPage])

        yuri = AdminPage(vkid=142872618)
        yuri.save()
    else:
        init_db()

        db_proxy.connect(True)
        print('CONNECTED')
        # TODO сделать так, чтобы дубликаты не добавлялись
        db_proxy.create_tables([AdminPage, TargetGroup, UserPage, SenderPage], safe=True)

        print('before AdminPage')
        yuri = AdminPage(vkid=142872618)
        yuri.save()

        print('before db.close()')
        db_proxy.close()

        return 'DB is created!'

def reset_db():
    import os, psycopg2, urllib.parse as urlparse  # CHECK
    urlparse.uses_netloc.append('postgres')
    url = urlparse.urlparse(os.environ["DATABASE_URL"])
    db = PostgresqlDatabase(database=url.path[1:], user=url.username, password=url.password, host=url.hostname,
                            port=url.port)

    db.connect(True)
    print('CONNECTED')

    db.drop_tables([AdminPage, TargetGroup, UserPage, SenderPage])

    db.create_tables([AdminPage, TargetGroup, UserPage, SenderPage])

    return 'DB is reseted!'
