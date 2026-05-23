from typing import Dict, List, Optional, Tuple

from app.db import get_db
from app.discs.models import Disc


def _find_many(query: dict, page: int, size: int) -> Tuple[List[Disc], int]:
    db = get_db()
    collection = db['discs']
    total = collection.count_documents(query)
    skip = (page - 1) * size
    discs_data = list(
        collection.find(query, {'_id': 0}).sort('author', 1).skip(skip).limit(size)
    )

    return [Disc(**disc) for disc in discs_data], total


def build_discs_query(type_value: Optional[str] = None, favorite: bool = False) -> Dict[str, object]:
    query: Dict[str, object] = {'enabled': True}

    if type_value is not None:
        query['type'] = type_value

    if favorite:
        query['favorite'] = True

    return query


def find_all(page: int, size: int) -> Tuple[List[Disc], int]:
    return _find_many(build_discs_query(), page, size)


def find_by_sku(sku: str) -> Optional[Disc]:
    db = get_db()
    disc_data = db['discs'].find_one({'sku': sku}, {'_id': 0})
    
    if disc_data is None:
        return None
    
    return Disc(**disc_data)


def find_by_type(type: str, page: int, size: int) -> Tuple[List[Disc], int]:
    return _find_many(build_discs_query(type_value=type), page, size)


def find_favorite(page: int, size: int) -> Tuple[List[Disc], int]:
    return _find_many(build_discs_query(favorite=True), page, size)


def find_discs(type_value: Optional[str], favorite: bool, page: int, size: int) -> Tuple[List[Disc], int]:
    return _find_many(build_discs_query(type_value=type_value, favorite=favorite), page, size)


def save(disc: dict):
    db = get_db()
    result = db['discs'].insert_one(disc)  # type: ignore
    
    return result.inserted_id