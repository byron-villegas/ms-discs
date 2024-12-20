from app.db import get_db

def find_all():
    db = get_db()
    discs = list(db['discs'].find({}, {'_id': 0}))

    return discs

def find_by_sku(sku: str):
    db = get_db()
    disc = db['discs'].find_one({'sku': sku}, {'_id': 0})

    return disc

def find_by_type(type: str):
    db = get_db()
    discs = list(db['discs'].find({'type': type}, {'_id': 0}))

    return discs

def find_favorite():
    db = get_db()
    discs = list(db['discs'].find({'favorite': True}, {'_id': 0}))

    return discs