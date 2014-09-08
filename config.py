class Config:
    API_URL = "http://localhost:5000"

class DevConfig(Config):
    pass

class PLGConfig(DevConfig):
    API_URL = "http://cersei-web-2.bitvid.tv:5000"