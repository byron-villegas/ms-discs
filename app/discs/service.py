
import re
from math import ceil
from typing import Optional

from flask import abort, jsonify, make_response
from app.exceptions.error_negocio_exception import ErrorNegocioException
from app.discs import repository
from app.discs.models import Disc

def _validate_pagination(page: int, size: int):
    if page < 1 or size < 1:
        abort(make_response(jsonify({"page": "page y size deben ser mayores que cero"}), 400))


def _build_paginated_response(discs, page: int, size: int, total_items: int):
    total_pages = ceil(total_items / size) if total_items > 0 else 0

    return {
        "items": [disc.model_dump() for disc in discs],
        "page": page,
        "size": size,
        "totalItems": total_items,
        "totalPages": total_pages,
    }


def get_discs(page: int = 1, size: int = 15):
    _validate_pagination(page, size)
    discs, total_items = repository.find_discs(None, False, page, size)

    return _build_paginated_response(discs, page, size, total_items)

def get_discs_by_type(type: str, page: int = 1, size: int = 15):
    _validate_pagination(page, size)
    pattern = re.compile(r"[A-Za-z0-9]+")

    if not re.fullmatch(pattern, type):
        abort(make_response(jsonify({"type": "Solo admite letras y numeros"}), 400))

    discs, total_items = repository.find_discs(type, False, page, size)

    return _build_paginated_response(discs, page, size, total_items)

def get_favorite_discs(page: int = 1, size: int = 15):
    _validate_pagination(page, size)
    discs, total_items = repository.find_discs(None, True, page, size)

    return _build_paginated_response(discs, page, size, total_items)


def get_filtered_discs(
    type: Optional[str] = None,
    favorite: bool = False,
    page: int = 1,
    size: int = 15,
    order_field: str = "author",
    order_direction: int = 1,
):
    _validate_pagination(page, size)

    if type is not None:
        pattern = re.compile(r"[A-Za-z0-9]+")

        if not re.fullmatch(pattern, type):
            abort(make_response(jsonify({"type": "Solo admite letras y numeros"}), 400))

    sort_field = "yearCreated" if order_field == "year" else order_field
    discs, total_items = repository.find_discs(type, favorite, page, size, sort_field, order_direction)

    return _build_paginated_response(discs, page, size, total_items)

def find_by_sku(sku: str):
    disc = repository.find_by_sku(sku)

    if disc is None:
        raise ErrorNegocioException("EXDNE01", "Disco no encontrado")

    return disc.model_dump()

def save_disc(disc_data: dict):
    # Validar con Pydantic
    disc = Disc(**disc_data)
    
    # Verificar si ya existe
    existing_disc = repository.find_by_sku(disc.sku)
    
    if existing_disc is not None:
        raise ErrorNegocioException("EXDYE01", "Disco ya existe")
    
    # Guardar en la base de datos
    repository.save(disc.model_dump())
    
    return disc