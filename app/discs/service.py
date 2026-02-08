
import re

from flask import abort, jsonify, make_response
from app.exceptions.error_negocio_exception import ErrorNegocioException
from app.discs import repository
from app.discs.models import Disc

def get_discs():
    discs = repository.find_all()
    
    return [disc.model_dump() for disc in discs]

def get_discs_by_type(type: str):
    pattern = re.compile(r"[A-Za-z0-9]+")

    if not re.fullmatch(pattern, type):
        abort(make_response(jsonify({"type": "Solo admite letras y numeros"}), 400))

    discs = repository.find_by_type(type)
    
    return [disc.model_dump() for disc in discs]

def get_favorite_discs():
    discs = repository.find_favorite()
    
    return [disc.model_dump() for disc in discs]

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