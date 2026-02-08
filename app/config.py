import os
import platform
import flask
from dotenv import load_dotenv

class Config:
    load_dotenv()
    SERVER_PATH = "/api"
    SERVER_PORT = "5000"
    SWAGGER_URL = '/swagger-ui'
    SWAGGER_FILE = "/static/swagger.yml"
    SECRET_KEY = os.environ.get("SECRET_KEY")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    MONGO_USER = os.environ.get("MONGO_USER")
    MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")
    MONGO_HOST = os.environ.get("MONGO_HOST")
    MONGO_DB = os.environ.get("MONGO_DB")
    MONGO_URI = "mongodb+srv://{0}:{1}@{2}/{3}".format(MONGO_USER, MONGO_PASSWORD, MONGO_HOST, MONGO_DB)
    CORS_ORIGIN = os.environ.get("CORS_ORIGIN")
    CORS_HEADERS = "Content-Type"

def showBanner():
    try:
        banner_path = os.path.join(os.path.abspath(os.path.dirname(__file__)).replace("app", ""), "banner.txt")
        if not os.path.exists(banner_path):
            return  # Skip banner in production/serverless environments
            
        with open(banner_path, "r") as bannerFile:
            bannerLog = bannerFile.read()

        bannerLog = bannerLog.replace("package.name", "ms-discs")
        bannerLog = bannerLog.replace("package.version", "1.0.0")
        bannerLog = bannerLog.replace("python.version", platform.python_version())
        bannerLog = bannerLog.replace("flask.version", flask.__version__)
        bannerLog = bannerLog.replace("server.path", Config.SERVER_PATH)
        bannerLog = bannerLog.replace("server.port", Config.SERVER_PORT)

        print(bannerLog)
    except Exception:
        # Silently skip banner in production/serverless environments
        pass

showBanner()