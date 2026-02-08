from app.db import get_db
from app.discs.models import Disc
from typing import List, Optional


def find_all() -> List[Disc]:
    db = get_db()
    discs_data = list(db['discs'].find({'enabled': True}, {'_id': 0}).sort('author', 1))
    
    return [Disc(**disc) for disc in discs_data]


def find_by_sku(sku: str) -> Optional[Disc]:
    db = get_db()
    disc_data = db['discs'].find_one({'sku': sku}, {'_id': 0})
    
    if disc_data is None:
        return None
    
    return Disc(**disc_data)


def find_by_type(type: str) -> List[Disc]:
    db = get_db()
    discs_data = list(db['discs'].find({'type': type, 'enabled': True}, {'_id': 0}).sort('author', 1))
    
    return [Disc(**disc) for disc in discs_data]


def find_favorite() -> List[Disc]:
    db = get_db()
    discs_data = list(db['discs'].find({'favorite': True, 'enabled': True}, {'_id': 0}).sort('author', 1))
    
    return [Disc(**disc) for disc in discs_data]


def save(disc: dict):
    db = get_db()
    result = db['discs'].insert_one(disc)  # type: ignore
    
    return result.inserted_id