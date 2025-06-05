from app.db import get_db

def find_all():
    db = get_db()
    discs = list(db['discs'].find({'enabled': True}, {'_id': 0}).sort('author', 1))

    return discs

def find_by_sku(sku: str):
    db = get_db()
    disc = db['discs'].find_one({'sku': sku}, {'_id': 0})

    return disc

def find_by_type(type: str):
    db = get_db()
    discs = list(db['discs'].find({'type': type, 'enabled': True}, {'_id': 0}).sort('author', 1))
    return discs

def find_favorite():
    db = get_db()
    discs = list(db['discs'].find({'favorite': True, 'enabled': True}, {'_id': 0}).sort('author', 1))

    return discs