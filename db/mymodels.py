from peewee import Model
from peewee import IntegerField
from peewee import ForeignKeyField
from peewee import TextField
from peewee import CharField
from peewee import PostgresqlDatabase, Proxy
from peewee import DateTimeField
from datetime import datetime

db_proxy = Proxy()

class TargetGroup(Model):
    vkid = IntegerField()
    admin_id = IntegerField()
    text = TextField()
    message_count = IntegerField()

    class Meta:
        database = db_proxy


class AdminPage(Model):
    vkid = IntegerField()
    # target_group = ForeignKeyField(TargetGroup, backref='id')

    class Meta:
        database = db_proxy


class UserPage(Model):
    vkid = IntegerField()
    target_group = ForeignKeyField(TargetGroup, backref='id')
    status = TextField() # 'not noticed', 'active'

    class Meta:
        database = db_proxy


class SenderPage(Model):
    vkid = IntegerField()
    token = TextField()
    message_count = IntegerField()
    update_time = DateTimeField(default=datetime(1999, 11, 23, 12, 30)) # мой день рождения.
                                            # При создании страницы обновляет message_count и update_time

    class Meta:
        database = db_proxy