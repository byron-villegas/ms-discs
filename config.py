import os
import platform
import flask

class Config:
    SERVER_PATH = "/api"
    SERVER_PORT = "5000"
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    CORS_HEADERS = "Content-Type"
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    MONGO_USER = os.environ.get('MONGO_USER')
    MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
    MONGO_HOST = os.environ.get('MONGO_HOST')
    MONGO_DB = os.environ.get('MONGO_DB')
    MONGO_URI = "mongodb+srv://{0}:{1}@{2}/{3}"

def showBanner(): 
    bannerFile = open(os.path.abspath(os.path.dirname(__file__)) + "/banner.txt", "r")
    bannerLog = bannerFile.read()
    bannerFile.close()

    bannerLog = bannerLog.replace("python.version", platform.python_version())
    bannerLog = bannerLog.replace("flask.version", flask.__version__)
    bannerLog = bannerLog.replace("server.path", Config.SERVER_PATH)
    bannerLog = bannerLog.replace("server.port", Config.SERVER_PORT)

    print(bannerLog)

showBanner()