# -*- coding: utf-8 -*-


class Config:
    API_URL = 'http://localhost:5000'
    SECRET_KEY = 'secret key'


class DevConfig(Config):
    HOST = 'http://localhost'
    DEBUG = True

class PLGConfig(DevConfig):
    API_URL = 'http://localhost:5000'
    HOST = "" #http://cersei-web-2.bitvid.tv/
