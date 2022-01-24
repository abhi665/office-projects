from flask_sqlalchemy import SQLAlchemy
import os
class Database:
    __x = None
    
    @classmethod
    def connect(self, app):
        DATABASE_URL_PGSQL=os.environ['DATABASE_URL']
        app.config['SQLALCHEMY_DATABASE_URI']= DATABASE_URL_PGSQL
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_POOL_SIZE'] = 10000000000000000000000000000000000000000000000
        app.config['connection_timeout'] = 10
        db = SQLAlchemy(app)
        self.__x = db
        return self.__x

    @classmethod
    def db(self):
        return self.__x
