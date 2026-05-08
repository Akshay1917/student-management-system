import mysql.connector
from mysql.connector import pooling
from flask import current_app, g
import os

class Database:
    _pool = None

    @classmethod
    def get_pool(cls):
        if cls._pool is None:
            config = {
                'host': current_app.config['MYSQL_HOST'],
                'user': current_app.config['MYSQL_USER'],
                'password': current_app.config['MYSQL_PASSWORD'],
                'database': current_app.config['MYSQL_DB'],
                'port': current_app.config['MYSQL_PORT'],
                'pool_name': 'sms_pool',
                'pool_size': 5,
            }
            cls._pool = mysql.connector.pooling.MySQLConnectionPool(**config)
        return cls._pool

    @classmethod
    def get_db(cls):
        if 'db' not in g:
            g.db = cls.get_pool().get_connection()
        return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)
