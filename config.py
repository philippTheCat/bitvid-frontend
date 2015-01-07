# -*- coding: utf-8 -*-

import os
class Config:
    API_URL = os.environ.get("API_URL",'http://bitvid-acc-backend.elasticbeanstalk.com/')
    SECRET_KEY = 'secret key'


class DevConfig(Config):
    HOST = 'http://localhost'
    DEBUG = True

class PLGConfig(DevConfig):
    API_URL = 'http://localhost:5000'
    HOST = "" #http://cersei-web-2.bitvid.tv/
