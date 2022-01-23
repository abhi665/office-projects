from flask_sqlalchemy import SQLAlchemy
import os
class Database:
    __x = None
    
    @classmethod
    def connect(self, app):
        DATABASE_URL_PGSQL=os.environ['DATABASE_URL']
        app.config['SQLALCHEMY_DATABASE_URI']= DATABASE_URL_PGSQL
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db = SQLAlchemy(app)
        self.__x = db
        return self.__x

    @classmethod
    def db(self):
        return self.__x
