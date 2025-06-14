from peewee import *

db = SqliteDatabase('data.db')


class User(Model):
    class Meta:
        database = db
        db_table = f'Users'

    vk_id = IntegerField()
    warns = IntegerField()
    chat = IntegerField()


if __name__ == '__main__':
    db.create_tables([User])