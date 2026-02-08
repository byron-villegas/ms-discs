from flask import current_app, g
from flask_pymongo import PyMongo
from pymongo.database import Database


def get_db() -> Database:
    if 'db' not in g:
        client = get_connection()
        g.db = client.db

    return g.db

def get_connection():
    client = PyMongo(current_app)
    return client