from flask_sqlalchemy import SQLAlchemy
# import os
class Database:
    __x = None
    
    @classmethod
    def connect(self, app):
        # app.config.from_object(os.environ['APP_SETTINGS'])
        app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:123@localhost:5432/HRM'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db = SQLAlchemy(app)
        self.__x = db
        return self.__x

    @classmethod
    def db(self):
        return self.__x
